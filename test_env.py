#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试Python环境和依赖
"""

print("Python环境测试开始...")

try:
    import flask
    print("✓ Flask 已安装")
except ImportError as e:
    print("✗ Flask 未安装:", e)

try:
    import flask_sqlalchemy
    print("✓ Flask-SQLAlchemy 已安装")
except ImportError as e:
    print("✗ Flask-SQLAlchemy 未安装:", e)

try:
    import flask_login
    print("✓ Flask-Login 已安装")
except ImportError as e:
    print("✗ Flask-Login 未安装:", e)

try:
    import flask_wtf
    print("✓ Flask-WTF 已安装")
except ImportError as e:
    print("✗ Flask-WTF 未安装:", e)

try:
    import wtforms
    print("✓ WTForms 已安装")
except ImportError as e:
    print("✗ WTForms 未安装:", e)

print("环境测试完成！")
