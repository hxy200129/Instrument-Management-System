#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建数据库表并插入测试数据
"""

from book_management_sys import app, db, Admin, Instrument, User, Inventory, UseInstrument
import time
import datetime

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 删除所有表
        db.drop_all()
        
        # 创建所有表
        db.create_all()
        
        # 添加管理员数据
        admin1 = Admin(
            admin_id='201801',
            admin_name='管理员',
            password='123456',
            right='超级管理员'
        )
        
        admin2 = Admin(
            admin_id='201802',
            admin_name='操作员',
            password='123456',
            right='普通管理员'
        )
        
        db.session.add(admin1)
        db.session.add(admin2)
        
        # 添加仪器信息
        instruments = [
            # 测量仪器类
            Instrument(
                instrument_id='1234567890001',
                instrument_name='数字万用表',
                manufacturer='福禄克',
                model='FLUKE-15B+',
                category='测量仪器'
            ),
            Instrument(
                instrument_id='1234567890002',
                instrument_name='示波器',
                manufacturer='泰克',
                model='TBS1052B',
                category='测量仪器'
            ),
            Instrument(
                instrument_id='1234567890003',
                instrument_name='频谱分析仪',
                manufacturer='罗德与施瓦茨',
                model='FSW26',
                category='测量仪器'
            ),
            Instrument(
                instrument_id='1234567890004',
                instrument_name='网络分析仪',
                manufacturer='安捷伦',
                model='E5071C',
                category='测量仪器'
            ),
            Instrument(
                instrument_id='1234567890005',
                instrument_name='逻辑分析仪',
                manufacturer='泰克',
                model='MSO64',
                category='测量仪器'
            ),
            # 信号源类
            Instrument(
                instrument_id='1234567890006',
                instrument_name='信号发生器',
                manufacturer='安捷伦',
                model='33220A',
                category='信号源'
            ),
            Instrument(
                instrument_id='1234567890007',
                instrument_name='任意波形发生器',
                manufacturer='是德科技',
                model='33622A',
                category='信号源'
            ),
            Instrument(
                instrument_id='1234567890008',
                instrument_name='射频信号发生器',
                manufacturer='罗德与施瓦茨',
                model='SMW200A',
                category='信号源'
            ),
            # 电源设备类
            Instrument(
                instrument_id='1234567890009',
                instrument_name='直流电源',
                manufacturer='是德科技',
                model='E3631A',
                category='电源设备'
            ),
            Instrument(
                instrument_id='1234567890010',
                instrument_name='可编程电源',
                manufacturer='吉时利',
                model='2230G-30-1',
                category='电源设备'
            ),
            Instrument(
                instrument_id='1234567890011',
                instrument_name='电子负载',
                manufacturer='艾德克斯',
                model='IT8512A+',
                category='电源设备'
            ),
            # 环境测试设备
            Instrument(
                instrument_id='1234567890012',
                instrument_name='温湿度计',
                manufacturer='德图',
                model='testo 175 H1',
                category='环境测试'
            ),
            Instrument(
                instrument_id='1234567890013',
                instrument_name='噪声计',
                manufacturer='普尔声',
                model='AWA5688',
                category='环境测试'
            ),
            # 机械测试设备
            Instrument(
                instrument_id='1234567890014',
                instrument_name='游标卡尺',
                manufacturer='三丰',
                model='500-196-30',
                category='机械测量'
            ),
            Instrument(
                instrument_id='1234567890015',
                instrument_name='千分尺',
                manufacturer='三丰',
                model='103-137',
                category='机械测量'
            ),
            # 光学设备
            Instrument(
                instrument_id='1234567890016',
                instrument_name='光功率计',
                manufacturer='安立',
                model='ML9001A',
                category='光学测量'
            ),
            Instrument(
                instrument_id='1234567890017',
                instrument_name='光谱分析仪',
                manufacturer='横河',
                model='AQ6370D',
                category='光学测量'
            ),
            # 化学分析设备
            Instrument(
                instrument_id='1234567890018',
                instrument_name='pH计',
                manufacturer='梅特勒',
                model='FE28',
                category='化学分析'
            ),
            Instrument(
                instrument_id='1234567890019',
                instrument_name='电导率仪',
                manufacturer='哈纳',
                model='HI2030',
                category='化学分析'
            ),
            Instrument(
                instrument_id='1234567890020',
                instrument_name='紫外分光光度计',
                manufacturer='岛津',
                model='UV-1900i',
                category='化学分析'
            )
        ]
        
        for instrument in instruments:
            db.session.add(instrument)
        
        # 添加用户数据
        today = datetime.date.today()
        today_stamp = int(time.mktime(today.timetuple())) * 1000
        valid_date = today + datetime.timedelta(days=365)  # 一年后到期
        valid_stamp = int(time.mktime(valid_date.timetuple())) * 1000
        
        users = [
            # 研究生用户
            User(
                card_id='16000001',
                user_id='201901001',
                user_name='张三',
                sex='男',
                telephone='13800138001',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            User(
                card_id='16000002',
                user_id='201901002',
                user_name='李四',
                sex='女',
                telephone='13800138002',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            User(
                card_id='16000003',
                user_id='201901003',
                user_name='王五',
                sex='男',
                telephone='13800138003',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            # 本科生用户
            User(
                card_id='16000004',
                user_id='202001001',
                user_name='赵六',
                sex='女',
                telephone='13800138004',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            User(
                card_id='16000005',
                user_id='202001002',
                user_name='钱七',
                sex='男',
                telephone='13800138005',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            User(
                card_id='16000006',
                user_id='202001003',
                user_name='孙八',
                sex='女',
                telephone='13800138006',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            User(
                card_id='16000007',
                user_id='202001004',
                user_name='周九',
                sex='男',
                telephone='13800138007',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            User(
                card_id='16000008',
                user_id='202001005',
                user_name='吴十',
                sex='女',
                telephone='13800138008',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            # 教师用户
            User(
                card_id='16000009',
                user_id='T001',
                user_name='陈教授',
                sex='男',
                telephone='13800138009',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            User(
                card_id='16000010',
                user_id='T002',
                user_name='林博士',
                sex='女',
                telephone='13800138010',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=False,
                debt=False
            ),
            # 有问题的用户（用于测试）
            User(
                card_id='16000011',
                user_id='202001006',
                user_name='测试用户1',
                sex='男',
                telephone='13800138011',
                enroll_date=str(today_stamp),
                valid_date=str(today_stamp - 86400000),  # 已过期
                loss=False,
                debt=True  # 欠费
            ),
            User(
                card_id='16000012',
                user_id='202001007',
                user_name='测试用户2',
                sex='女',
                telephone='13800138012',
                enroll_date=str(today_stamp),
                valid_date=str(valid_stamp),
                loss=True,  # 已挂失
                debt=False
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        # 添加库存数据
        inventory_items = []
        barcode_counter = 1

        # 为每个仪器添加多个库存项
        for i, instrument in enumerate(instruments):
            # 每种仪器添加2-5个库存项
            count = 2 + (i % 4)  # 2-5个
            for j in range(count):
                status = True
                if i < 5 and j == 0:  # 前5种仪器的第一个设备设为已借出
                    status = False

                location_areas = ['A区', 'B区', 'C区', 'D区']
                location = f"{location_areas[i % 4]}-{(j+1):02d}架"

                inventory_items.append(Inventory(
                    barcode=f'{barcode_counter:06d}',
                    instrument_id=instrument.instrument_id,
                    storage_date=str(today_stamp),
                    location=location,
                    withdraw=False,
                    status=status,
                    admin='201801'
                ))
                barcode_counter += 1
        
        for item in inventory_items:
            db.session.add(item)
        
        # 添加借用记录
        use_records = []

        # 当前借用记录（未归还）
        current_borrows = [
            ('000001', '16000001', 10, 30),  # 张三借数字万用表，10天前借，30天后到期
            ('000003', '16000002', 5, 25),   # 李四借示波器，5天前借，25天后到期
            ('000006', '16000009', 15, 35),  # 陈教授借信号发生器，15天前借，35天后到期
            ('000011', '16000004', 3, 27),   # 赵六借任意波形发生器，3天前借，27天后到期
            ('000016', '16000005', 7, 33),   # 钱七借直流电源，7天前借，33天后到期
        ]

        for barcode, card_id, days_ago, days_until_due in current_borrows:
            borrow_date = today - datetime.timedelta(days=days_ago)
            borrow_stamp = int(time.mktime(borrow_date.timetuple())) * 1000
            due_date = today + datetime.timedelta(days=days_until_due)
            due_stamp = int(time.mktime(due_date.timetuple())) * 1000

            use_records.append(UseInstrument(
                barcode=barcode,
                card_id=card_id,
                start_date=str(borrow_stamp),
                borrow_admin='201801',
                end_date=None,  # 未归还
                return_admin=None,
                due_date=str(due_stamp)
            ))

        # 历史借用记录（已归还）
        historical_borrows = [
            ('000002', '16000001', 30, 25, 20),  # 张三借过数字万用表，30天前借，25天前还
            ('000004', '16000002', 45, 40, 35),  # 李四借过示波器，45天前借，40天前还
            ('000007', '16000003', 60, 55, 50),  # 王五借过频谱分析仪，60天前借，55天前还
            ('000012', '16000006', 35, 30, 25),  # 孙八借过温湿度计，35天前借，30天前还
            ('000018', '16000007', 50, 45, 40),  # 周九借过pH计，50天前借，45天前还
            ('000005', '16000008', 25, 20, 15),  # 吴十借过网络分析仪，25天前借，20天前还
            ('000009', '16000010', 40, 35, 30),  # 林博士借过可编程电源，40天前借，35天前还
        ]

        for barcode, card_id, borrow_days_ago, due_days_ago, return_days_ago in historical_borrows:
            borrow_date = today - datetime.timedelta(days=borrow_days_ago)
            borrow_stamp = int(time.mktime(borrow_date.timetuple())) * 1000
            due_date = today - datetime.timedelta(days=due_days_ago)
            due_stamp = int(time.mktime(due_date.timetuple())) * 1000
            return_date = today - datetime.timedelta(days=return_days_ago)
            return_stamp = int(time.mktime(return_date.timetuple())) * 1000

            use_records.append(UseInstrument(
                barcode=barcode,
                card_id=card_id,
                start_date=str(borrow_stamp),
                borrow_admin='201801',
                end_date=str(return_stamp),
                return_admin='201802',
                due_date=str(due_stamp)
            ))

        for record in use_records:
            db.session.add(record)
        
        # 提交所有更改
        db.session.commit()
        
        print("=" * 50)
        print("🎉 数据库初始化完成！")
        print("=" * 50)
        print("👤 管理员账号:")
        print("   - 超级管理员: 201801 / 123456")
        print("   - 普通管理员: 201802 / 123456")
        print()
        print("👥 测试用户 (共12个):")
        print("   - 研究生: 16000001-16000003")
        print("   - 本科生: 16000004-16000008")
        print("   - 教师: 16000009-16000010")
        print("   - 测试用户: 16000011-16000012 (有问题账户)")
        print()
        print("🔬 仪器设备 (共20种类型):")
        print("   - 测量仪器: 数字万用表, 示波器, 频谱分析仪等")
        print("   - 信号源: 信号发生器, 任意波形发生器等")
        print("   - 电源设备: 直流电源, 可编程电源等")
        print("   - 环境测试: 温湿度计, 噪声计")
        print("   - 机械测量: 游标卡尺, 千分尺")
        print("   - 光学测量: 光功率计, 光谱分析仪")
        print("   - 化学分析: pH计, 电导率仪, 紫外分光光度计")
        print()
        print("📊 数据统计:")
        print(f"   - 仪器种类: {len(instruments)} 种")
        print(f"   - 库存设备: {len(inventory_items)} 台")
        print(f"   - 注册用户: {len(users)} 人")
        print(f"   - 借用记录: {len(use_records)} 条")
        print()
        print("🌐 访问地址: http://127.0.0.1:5000")
        print("=" * 50)

if __name__ == '__main__':
    init_database()
