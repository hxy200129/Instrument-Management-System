#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys

def test_route(url, description):
    """测试路由是否可访问"""
    try:
        response = requests.get(url, allow_redirects=False, timeout=5)
        if response.status_code == 200:
            print(f"✅ {description}: 正常访问 (200)")
            return True
        elif response.status_code == 302:
            print(f"🔄 {description}: 重定向到登录页 (302) - 正常")
            return True
        else:
            print(f"❌ {description}: 状态码 {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {description}: 连接错误 - {e}")
        return False

def main():
    base_url = "http://127.0.0.1:5000"
    
    print("=== 测试仪器管理四个功能的路由 ===\n")
    
    # 测试四个功能路由
    routes_to_test = [
        ("/new_store", "📝 新仪器登记"),
        ("/storage", "📦 设备入库"),
        ("/borrow", "📤 仪器借用"),
        ("/return", "📥 归还仪器"),
    ]
    
    success_count = 0
    for route, desc in routes_to_test:
        if test_route(f"{base_url}{route}", desc):
            success_count += 1
    
    print(f"\n测试结果: {success_count}/{len(routes_to_test)} 个路由正常")
    
    if success_count == len(routes_to_test):
        print("🎉 所有路由都正常工作！")
    else:
        print("⚠️  有路由存在问题，请检查")

if __name__ == "__main__":
    main()
