from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class Login(FlaskForm):
    account = StringField(u'账号', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'登录')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[DataRequired(), EqualTo('password2', message=u'两次密码必须一致！')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'确认修改')


class EditInfoForm(FlaskForm):
    name = StringField(u'用户名', validators=[Length(1, 32)])
    submit = SubmitField(u'提交')


class SearchInstrumentForm(FlaskForm):
    methods = [('instrument_name', '仪器名称'), ('manufacturer', '制造商'), ('category', '类别'), ('instrument_id', '仪器编号')]
    method = SelectField(choices=methods, validators=[DataRequired()], coerce=str)
    content = StringField(validators=[DataRequired()])
    submit = SubmitField('搜索')


class SearchUserForm(FlaskForm):
    card = StringField(validators=[DataRequired()])
    submit = SubmitField('搜索')


class StoreForm(FlaskForm):
    barcode = StringField(validators=[DataRequired(), Length(6)])
    instrument_id = StringField(validators=[DataRequired(), Length(13)])
    location = StringField(validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField(u'提交')


class NewStoreForm(FlaskForm):
    instrument_id = StringField(validators=[DataRequired(), Length(13)])
    instrument_name = StringField(validators=[DataRequired(), Length(1, 64)])
    manufacturer = StringField(validators=[DataRequired(), Length(1, 64)])
    model = StringField(validators=[DataRequired(), Length(1, 32)])
    category = StringField(validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField(u'提交')


class BorrowForm(FlaskForm):
    card = StringField(validators=[DataRequired()])
    instrument_name = StringField(validators=[DataRequired()])
    submit = SubmitField(u'搜索')


class ReturnForm(FlaskForm):
    card = StringField(validators=[DataRequired()])
    submit = SubmitField(u'搜索')
