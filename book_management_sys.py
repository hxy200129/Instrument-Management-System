from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from forms import Login, SearchInstrumentForm, ChangePasswordForm, EditInfoForm, SearchUserForm, NewStoreForm, StoreForm, BorrowForm, ReturnForm
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
import time, datetime

def timeStamp(timeNum):
    timeArray = time.localtime(int(timeNum) / 1000)
    return time.strftime("%Y-%m-%d", timeArray)


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SERVER_NAME'] = '127.0.0.1:5000'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.login_message = u"请先登录。"


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(6), primary_key=True)
    admin_name = db.Column(db.String(32))
    password = db.Column(db.String(24))
    right = db.Column(db.String(32))

    def __init__(self, admin_id, admin_name, password, right):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.password = password
        self.right = right

    def get_id(self):
        return self.admin_id

    def verify_password(self, password):
        if password == self.password:
            return True
        else:
            return False

    def __repr__(self):
        return '<Admin %r>' % self.admin_name


class Instrument(db.Model):
    __tablename__ = 'instrument'
    instrument_id = db.Column(db.String(13), primary_key=True)
    instrument_name = db.Column(db.String(64))
    manufacturer = db.Column(db.String(64))
    model = db.Column(db.String(32))
    category = db.Column(db.String(64))

    def __repr__(self):
        return '<Instrument %r>' % self.instrument_name


class User(db.Model):
    __tablename__ = 'user'
    card_id = db.Column(db.String(8), primary_key=True)
    user_id = db.Column(db.String(9))
    user_name = db.Column(db.String(32))
    sex = db.Column(db.String(2))
    telephone = db.Column(db.String(11), nullable=True)
    enroll_date = db.Column(db.String(13))
    valid_date = db.Column(db.String(13))
    loss = db.Column(db.Boolean, default=False)  # 是否挂失
    debt = db.Column(db.Boolean, default=False)  # 是否欠费

    def __repr__(self):
        return '<User %r>' % self.user_name


class Inventory(db.Model):
    __tablename__ = 'inventory'
    barcode = db.Column(db.String(6), primary_key=True)
    instrument_id = db.Column(db.ForeignKey('instrument.instrument_id'))
    storage_date = db.Column(db.String(13))
    location = db.Column(db.String(32))
    withdraw = db.Column(db.Boolean, default=False)  # 是否注销
    status = db.Column(db.Boolean, default=True)  # 是否在库
    admin = db.Column(db.ForeignKey('admin.admin_id'))  # 入库操作员

    def __repr__(self):
        return '<Inventory %r>' % self.barcode


class UseInstrument(db.Model):
    __tablename__ = 'useinstrument'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.ForeignKey('inventory.barcode'), index=True)
    card_id = db.Column(db.ForeignKey('user.card_id'), index=True)
    start_date = db.Column(db.String(13))
    borrow_admin = db.Column(db.ForeignKey('admin.admin_id'))  # 借出操作员
    end_date = db.Column(db.String(13), nullable=True)
    return_admin = db.Column(db.ForeignKey('admin.admin_id'))  # 归还操作员
    due_date = db.Column(db.String(13))  # 应还日期

    def __repr__(self):
        return '<UseInstrument %r>' % self.id


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))


@app.route('/', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = Admin.query.filter_by(admin_id=form.account.data, password=form.password.data).first()
        if user is None:
            flash('账号或密码错误！')
            return redirect(url_for('login'))
        else:
            login_user(user)
            session['admin_id'] = user.admin_id
            session['name'] = user.admin_name
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出！')
    return redirect(url_for('login'))


@app.route('/index')
@login_required
def index():
    return render_template('index.html', name=session.get('name'))



@app.route('/user/<id>')
@login_required
def user_info(id):
    user = Admin.query.filter_by(admin_id=id).first()
    return render_template('user-info.html', user=user, name=session.get('name'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.password2.data != form.password.data:
        flash(u'两次密码不一致！')
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'已成功修改密码！')
            return redirect(url_for('index'))
        else:
            flash(u'原密码输入错误，修改失败！')
    return render_template("change-password.html", form=form)


@app.route('/change_info', methods=['GET', 'POST'])
@login_required
def change_info():
    form = EditInfoForm()
    if form.validate_on_submit():
        current_user.admin_name = form.name.data
        db.session.add(current_user)
        flash(u'已成功修改个人信息！')
        return redirect(url_for('user_info', id=current_user.admin_id))
    form.name.data = current_user.admin_name
    id = current_user.admin_id
    right = current_user.right
    return render_template('change-info.html', form=form, id=id, right=right)


@app.route('/search_instrument', methods=['GET', 'POST'])
@login_required
def search_instrument():
    form = SearchInstrumentForm()
    return render_template('search-instrument.html', name=session.get('name'), form=form)


@app.route('/instruments', methods=['POST'])
def find_instrument():
    def find_name():
        return Instrument.query.filter(Instrument.instrument_name.like('%'+request.form.get('content')+'%')).all()

    def find_manufacturer():
        return Instrument.query.filter(Instrument.manufacturer.contains(request.form.get('content'))).all()

    def find_category():
        return Instrument.query.filter(Instrument.category.contains(request.form.get('content'))).all()

    def find_id():
        return Instrument.query.filter(Instrument.instrument_id.contains(request.form.get('content'))).all()

    methods = {
        'instrument_name': find_name,
        'manufacturer': find_manufacturer,
        'category': find_category,
        'instrument_id': find_id
    }
    instruments = methods[request.form.get('method')]()
    data = []
    for instrument in instruments:
        count = Inventory.query.filter_by(instrument_id=instrument.instrument_id).count()
        available = Inventory.query.filter_by(instrument_id=instrument.instrument_id, status=True).count()
        item = {'instrument_id': instrument.instrument_id, 'instrument_name': instrument.instrument_name, 
                'model': instrument.model, 'manufacturer': instrument.manufacturer,
                'category': instrument.category, 'count': count, 'available': available}
        data.append(item)
    return jsonify(data)




@app.route('/storage', methods=['GET', 'POST'])
@login_required
def storage():
    form = StoreForm()
    if form.validate_on_submit():
        instrument = Instrument.query.filter_by(instrument_id=request.form.get('instrument_id')).first()
        exist = Inventory.query.filter_by(barcode=request.form.get('barcode')).first()
        if instrument is None:
            flash(u"添加失败，请注意本仪器信息是否已录入，若未登记，请在'新仪器入库'窗口录入信息。")
        else:
            if len(request.form.get('barcode')) != 6:
                flash(u'仪器编码长度错误')
            else:
                if exist is not None:
                    flash(u'该编号已经存在！')
                else:
                    item = Inventory()
                    item.barcode = request.form.get('barcode')
                    item.instrument_id = request.form.get('instrument_id')
                    item.admin = current_user.admin_id
                    item.location = request.form.get('location')
                    item.status = True
                    item.withdraw = False
                    today_date = datetime.date.today()
                    today_str = today_date.strftime("%Y-%m-%d")
                    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
                    item.storage_date = int(today_stamp)*1000
                    db.session.add(item)
                    db.session.commit()
                    flash(u'入库成功！')
        return redirect(url_for('storage'))
    return render_template('storage.html', name=session.get('name'), form=form)


@app.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = NewStoreForm()
    if form.validate_on_submit():
        if len(request.form.get('instrument_id')) != 13:
            flash(u'仪器编号长度错误')
        else:
            exist = Instrument.query.filter_by(instrument_id=request.form.get('instrument_id')).first()
            if exist is not None:
                flash(u'该仪器信息已经存在，请核对后再录入；或者填写入库表。')
            else:
                instrument = Instrument()
                instrument.instrument_id = request.form.get('instrument_id')
                instrument.instrument_name = request.form.get('instrument_name')
                instrument.manufacturer = request.form.get('manufacturer')
                instrument.model = request.form.get('model')
                instrument.category = request.form.get('category')
                db.session.add(instrument)
                db.session.commit()
                flash(u'仪器信息添加成功！')
        return redirect(url_for('new_store'))
    return render_template('new-store.html', name=session.get('name'), form=form)


@app.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    form = BorrowForm()
    return render_template('borrow.html', name=session.get('name'), form=form)


@app.route('/find_stu_instrument', methods=['GET', 'POST'])
def find_stu_instrument():
    stu = User.query.filter_by(card_id=request.form.get('card')).first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    if stu is None:
        return jsonify([{'stu': 0}])  # 没找到
    if stu.debt is True:
        return jsonify([{'stu': 1}])  # 欠费
    if int(stu.valid_date) < int(today_stamp)*1000:
        return jsonify([{'stu': 2}])  # 到期
    if stu.loss is True:
        return jsonify([{'stu': 3}])  # 已经挂失
    instruments = db.session.query(Instrument).join(Inventory).filter(Instrument.instrument_name.contains(request.form.get('instrument_name')),
        Inventory.status == 1).with_entities(Inventory.barcode, Instrument.instrument_id, Instrument.instrument_name, Instrument.manufacturer, Instrument.model).\
        all()
    data = []
    for instrument in instruments:
        item = {'barcode': instrument.barcode, 'instrument_id': instrument.instrument_id, 'instrument_name': instrument.instrument_name,
                'manufacturer': instrument.manufacturer, 'model': instrument.model}
        data.append(item)
    return jsonify(data)


@app.route('/out', methods=['GET', 'POST'])
@login_required
def out():
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    barcode = request.args.get('barcode')
    card = request.args.get('card')
    instrument_name = request.args.get('instrument_name')
    useinstrument = UseInstrument()
    useinstrument.barcode = barcode
    useinstrument.card_id = card
    useinstrument.start_date = int(today_stamp)*1000
    useinstrument.due_date = (int(today_stamp)+40*86400)*1000
    useinstrument.borrow_admin = current_user.admin_id
    db.session.add(useinstrument)
    db.session.commit()
    instrument = Inventory.query.filter_by(barcode=barcode).first()
    instrument.status = False
    db.session.add(instrument)
    db.session.commit()
    bks = db.session.query(Instrument).join(Inventory).filter(Instrument.instrument_name.contains(instrument_name), Inventory.status == 1).\
        with_entities(Inventory.barcode, Instrument.instrument_id, Instrument.instrument_name, Instrument.manufacturer, Instrument.model).all()
    data = []
    for bk in bks:
        item = {'barcode': bk.barcode, 'instrument_id': bk.instrument_id, 'instrument_name': bk.instrument_name,
                'manufacturer': bk.manufacturer, 'model': bk.model}
        data.append(item)
    return jsonify(data)


@app.route('/return', methods=['GET', 'POST'])
@login_required
def return_instrument():
    form = ReturnForm()
    return render_template('return.html', name=session.get('name'), form=form)


@app.route('/find_not_return_instrument', methods=['GET', 'POST'])
def find_not_return_instrument():
    stu = User.query.filter_by(card_id=request.form.get('card')).first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    if stu is None:
        return jsonify([{'stu': 0}])  # 没找到
    if stu.debt is True:
        return jsonify([{'stu': 1}])  # 欠费
    if int(stu.valid_date) < int(today_stamp)*1000:
        return jsonify([{'stu': 2}])  # 到期
    if stu.loss is True:
        return jsonify([{'stu': 3}])  # 已经挂失
    instruments = db.session.query(UseInstrument).join(Inventory).join(Instrument).filter(UseInstrument.card_id == request.form.get('card'),
        UseInstrument.end_date.is_(None)).with_entities(UseInstrument.barcode, Instrument.instrument_id, Instrument.instrument_name, UseInstrument.start_date,
                                                 UseInstrument.due_date).all()
    data = []
    for instrument in instruments:
        start_date = timeStamp(instrument.start_date)
        due_date = timeStamp(instrument.due_date)
        item = {'barcode': instrument.barcode, 'instrument_id': instrument.instrument_id, 'instrument_name': instrument.instrument_name,
                'start_date': start_date, 'due_date': due_date}
        data.append(item)
    return jsonify(data)


@app.route('/in', methods=['GET', 'POST'])
@login_required
def instrumentin():
    barcode = request.args.get('barcode')
    card = request.args.get('card')
    record = UseInstrument.query.filter(UseInstrument.barcode == barcode, UseInstrument.card_id == card, UseInstrument.end_date.is_(None)).\
        first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    record.end_date = int(today_stamp)*1000
    record.return_admin = current_user.admin_id
    db.session.add(record)
    db.session.commit()
    instrument = Inventory.query.filter_by(barcode=barcode).first()
    instrument.status = True
    db.session.add(instrument)
    db.session.commit()
    bks = db.session.query(UseInstrument).join(Inventory).join(Instrument).filter(UseInstrument.card_id == card,
        UseInstrument.end_date.is_(None)).with_entities(UseInstrument.barcode, Instrument.instrument_id, Instrument.instrument_name, UseInstrument.start_date,
                                                 UseInstrument.due_date).all()
    data = []
    for bk in bks:
        start_date = timeStamp(bk.start_date)
        due_date = timeStamp(bk.due_date)
        item = {'barcode': bk.barcode, 'instrument_id': bk.instrument_id, 'instrument_name': bk.instrument_name,
                'start_date': start_date, 'due_date': due_date}
        data.append(item)
    return jsonify(data)


@app.route('/search_student', methods=['GET', 'POST'])
@login_required
def search_student():
    form = SearchUserForm()
    return render_template('search-student.html', form=form)


@app.route('/find_student', methods=['POST'])
def find_student():
    card_id = request.form.get('card')
    user = User.query.filter_by(card_id=card_id).first()
    if user is None:
        return jsonify([])

    data = [{
        'name': user.user_name,
        'gender': user.sex,
        'valid_date': timeStamp(user.valid_date),
        'debt': user.debt
    }]
    return jsonify(data)


@app.route('/find_record', methods=['POST'])
def find_record():
    card_id = request.form.get('card')
    records = db.session.query(UseInstrument).join(Inventory).join(Instrument).filter(
        UseInstrument.card_id == card_id
    ).with_entities(
        UseInstrument.barcode,
        Instrument.instrument_name,
        Instrument.manufacturer,
        UseInstrument.start_date,
        UseInstrument.due_date,
        UseInstrument.end_date
    ).all()

    data = []
    for record in records:
        end_date = timeStamp(record.end_date) if record.end_date else '未归还'
        item = {
            'barcode': record.barcode,
            'book_name': record.instrument_name,  # 保持与模板一致
            'author': record.manufacturer,  # 用制造商代替作者
            'start_date': timeStamp(record.start_date),
            'due_date': timeStamp(record.due_date),
            'end_date': end_date
        }
        data.append(item)
    return jsonify(data)





# API路由 - 数据分析
@app.route('/api/statistics')
def api_statistics():
    """获取系统统计数据"""
    try:
        # 仪器种类总数
        total_instruments = Instrument.query.count()

        # 可用设备数量
        available_instruments = Inventory.query.filter_by(status=True, withdraw=False).count()

        # 已借出设备数量
        borrowed_instruments = Inventory.query.filter_by(status=False, withdraw=False).count()

        # 注册用户总数
        total_users = User.query.count()

        # 逾期未还数量
        today_stamp = int(time.time()) * 1000
        overdue_count = UseInstrument.query.filter(
            UseInstrument.end_date.is_(None),
            UseInstrument.due_date < str(today_stamp)
        ).count()

        # 今日活动（今日借出和归还的总数）
        today_date = datetime.date.today()
        today_str = today_date.strftime("%Y-%m-%d")
        today_stamp_start = int(time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000

        today_borrows = UseInstrument.query.filter_by(start_date=str(today_stamp_start)).count()
        today_returns = UseInstrument.query.filter_by(end_date=str(today_stamp_start)).count()
        today_activity = today_borrows + today_returns

        return jsonify({
            'total_instruments': total_instruments,
            'available_instruments': available_instruments,
            'borrowed_instruments': borrowed_instruments,
            'total_users': total_users,
            'overdue_count': overdue_count,
            'today_activity': today_activity
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/trend-data')
def api_trend_data():
    """获取近10天借还趋势数据"""
    try:
        dates = []
        borrow_counts = []
        return_counts = []

        today_date = datetime.date.today()

        for i in range(9, -1, -1):  # 从10天前到今天
            date = today_date - datetime.timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            date_stamp = int(time.mktime(time.strptime(date_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000

            # 当天借出数量
            borrow_count = UseInstrument.query.filter_by(start_date=str(date_stamp)).count()

            # 当天归还数量
            return_count = UseInstrument.query.filter_by(end_date=str(date_stamp)).count()

            dates.append(date.strftime("%m-%d"))
            borrow_counts.append(borrow_count)
            return_counts.append(return_count)

        return jsonify({
            'dates': dates,
            'borrow_counts': borrow_counts,
            'return_counts': return_counts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/category-data')
def api_category_data():
    """获取仪器类别分布数据"""
    try:
        # 查询每个类别的仪器数量
        categories = db.session.query(
            Instrument.category,
            db.func.count(Instrument.instrument_id).label('count')
        ).group_by(Instrument.category).all()

        # 定义颜色
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c', '#34495e', '#95a5a6']

        data = []
        for i, (category, count) in enumerate(categories):
            data.append({
                'name': category,
                'value': count,
                'itemStyle': {'color': colors[i % len(colors)]}
            })

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/usage-data')
def api_usage_data():
    """获取设备使用率排行数据"""
    try:
        # 查询每种仪器的使用次数
        usage_stats = db.session.query(
            Instrument.instrument_name,
            db.func.count(UseInstrument.id).label('usage_count')
        ).join(Inventory, Instrument.instrument_id == Inventory.instrument_id)\
         .join(UseInstrument, Inventory.barcode == UseInstrument.barcode)\
         .group_by(Instrument.instrument_name)\
         .order_by(db.func.count(UseInstrument.id).desc())\
         .limit(10).all()

        names = [stat[0] for stat in usage_stats]
        values = [stat[1] for stat in usage_stats]

        return jsonify({
            'names': names,
            'values': values
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user-activity-data')
def api_user_activity_data():
    """获取用户活跃度数据"""
    try:
        # 查询每个用户的借用次数
        user_stats = db.session.query(
            User.user_name,
            db.func.count(UseInstrument.id).label('borrow_count')
        ).join(UseInstrument, User.card_id == UseInstrument.card_id)\
         .group_by(User.user_name)\
         .order_by(db.func.count(UseInstrument.id).desc())\
         .limit(10).all()

        names = [stat[0] for stat in user_stats]
        values = [stat[1] for stat in user_stats]

        return jsonify({
            'names': names,
            'values': values
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
