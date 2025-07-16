#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的Flask测试
"""

try:
    from flask import Flask
    print("✓ Flask导入成功")
    
    app = Flask(__name__)
    print("✓ Flask应用创建成功")
    
    @app.route('/')
    def hello():
        return '<h1>仪器管理系统测试页面</h1><p>系统运行正常！</p>'
    
    print("启动测试服务器...")
    print("访问地址: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
