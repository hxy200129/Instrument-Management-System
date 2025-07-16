#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
系统诊断脚本
"""

import sys
import os

print("=== 系统诊断 ===")
print(f"Python版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")
print(f"Python路径: {sys.executable}")

print("\n=== 检查依赖包 ===")
packages = ['flask', 'flask_sqlalchemy', 'flask_login', 'flask_wtf', 'wtforms']

for package in packages:
    try:
        __import__(package)
        print(f"✓ {package} - 已安装")
    except ImportError as e:
        print(f"✗ {package} - 未安装: {e}")

print("\n=== 检查文件 ===")
files = ['book_management_sys.py', 'forms.py', 'templates', 'static']

for file in files:
    if os.path.exists(file):
        print(f"✓ {file} - 存在")
    else:
        print(f"✗ {file} - 不存在")

print("\n=== 尝试导入主模块 ===")
try:
    import book_management_sys
    print("✓ book_management_sys 导入成功")
    
    # 尝试创建应用上下文
    with book_management_sys.app.app_context():
        print("✓ Flask应用上下文创建成功")
        
        # 尝试创建数据库表
        book_management_sys.db.create_all()
        print("✓ 数据库表创建成功")
        
except Exception as e:
    print(f"✗ 导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 诊断完成 ===")
