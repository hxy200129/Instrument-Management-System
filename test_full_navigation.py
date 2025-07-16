#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup

def test_login_and_navigation():
    """测试登录后的导航功能"""
    session = requests.Session()
    base_url = "http://127.0.0.1:5000"
    
    print("=== 完整导航功能测试 ===\n")
    
    # 1. 获取登录页面
    print("1. 获取登录页面...")
    try:
        login_page = session.get(f"{base_url}/")
        if login_page.status_code != 200:
            print(f"❌ 无法访问登录页面: {login_page.status_code}")
            return False
        print("✅ 登录页面访问正常")
    except Exception as e:
        print(f"❌ 登录页面访问失败: {e}")
        return False
    
    # 2. 解析CSRF token
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    if csrf_token:
        csrf_value = csrf_token.get('value')
        print("✅ 获取CSRF token成功")
    else:
        print("⚠️  未找到CSRF token，尝试无token登录")
        csrf_value = None
    
    # 3. 执行登录
    print("\n2. 执行登录...")
    login_data = {
        'account': '201801',
        'password': '123456'
    }
    if csrf_value:
        login_data['csrf_token'] = csrf_value
    
    try:
        login_response = session.post(f"{base_url}/", data=login_data, allow_redirects=False)
        if login_response.status_code == 302:
            print("✅ 登录成功，正在重定向")
        else:
            print(f"❌ 登录失败: {login_response.status_code}")
            print(f"响应内容: {login_response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return False
    
    # 4. 测试主页
    print("\n3. 测试主页访问...")
    try:
        index_response = session.get(f"{base_url}/index")
        if index_response.status_code == 200:
            print("✅ 主页访问正常")
        else:
            print(f"❌ 主页访问失败: {index_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 主页访问异常: {e}")
        return False
    
    # 5. 测试四个功能页面
    print("\n4. 测试四个功能页面...")
    test_pages = [
        ("/new_store", "📝 新仪器登记"),
        ("/storage", "📦 设备入库"),
        ("/borrow", "📤 仪器借用"),
        ("/return", "📥 归还仪器"),
    ]
    
    success_count = 0
    for path, name in test_pages:
        try:
            response = session.get(f"{base_url}{path}")
            if response.status_code == 200:
                print(f"✅ {name}: 访问正常")
                success_count += 1
            else:
                print(f"❌ {name}: 状态码 {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: 访问异常 - {e}")
    
    print(f"\n测试结果: {success_count}/{len(test_pages)} 个功能页面正常")
    
    if success_count == len(test_pages):
        print("🎉 所有功能页面都可以正常访问！")
        print("\n✅ 导航跳转问题已解决")
        return True
    else:
        print("⚠️  仍有页面存在问题")
        return False

if __name__ == "__main__":
    test_login_and_navigation()
