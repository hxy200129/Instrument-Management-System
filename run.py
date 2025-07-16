#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化的运行脚本
"""

from book_management_sys import app, db

if __name__ == '__main__':
    with app.app_context():
        # 创建数据库表
        db.create_all()
        print("数据库表已创建")
    
    print("启动仪器管理系统...")
    print("访问地址: http://127.0.0.1:5000")
    print("管理员账号: 201801, 密码: 123456")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
