#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup

def test_index_page():
    """专门测试系统概览页面"""
    session = requests.Session()
    base_url = "http://127.0.0.1:5000"
    
    print("=== 系统概览页面测试 ===\n")
    
    # 1. 登录
    print("1. 执行登录...")
    try:
        # 获取登录页面和CSRF token
        login_page = session.get(f"{base_url}/")
        soup = BeautifulSoup(login_page.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})
        csrf_value = csrf_token.get('value') if csrf_token else None
        
        # 登录
        login_data = {
            'account': '201801',
            'password': '123456'
        }
        if csrf_value:
            login_data['csrf_token'] = csrf_value
        
        login_response = session.post(f"{base_url}/", data=login_data, allow_redirects=False)
        if login_response.status_code == 302:
            print("✅ 登录成功")
        else:
            print("❌ 登录失败")
            return False
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return False
    
    # 2. 测试index页面直接访问
    print("\n2. 测试index页面直接访问...")
    try:
        response = session.get(f"{base_url}/index")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ index页面可以直接访问")
            
            # 检查页面内容
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            if title:
                print(f"页面标题: {title.text}")
            
            # 检查是否有真正的错误信息（排除JavaScript代码中的错误处理）
            error_patterns = [
                "500 Internal Server Error",
                "404 Not Found",
                "Traceback",
                "Exception:",
                "Error:",
                "Failed to"
            ]

            has_error = False
            for pattern in error_patterns:
                if pattern in response.text:
                    print(f"⚠️  页面包含错误信息: {pattern}")
                    has_error = True
                    break

            if not has_error:
                print("✅ 页面内容正常")
                
        else:
            print(f"❌ index页面访问失败: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ index页面访问异常: {e}")
        return False
    
    # 3. 测试从登录后的重定向
    print("\n3. 测试登录重定向...")
    try:
        # 重新登录，这次跟随重定向
        login_response = session.post(f"{base_url}/", data=login_data, allow_redirects=True)
        print(f"最终URL: {login_response.url}")
        print(f"状态码: {login_response.status_code}")
        
        if "/index" in login_response.url and login_response.status_code == 200:
            print("✅ 登录重定向到index页面正常")
        else:
            print("❌ 登录重定向有问题")
            
    except Exception as e:
        print(f"❌ 登录重定向测试异常: {e}")
        return False
    
    print("\n🎉 系统概览页面测试完成")
    return True

if __name__ == "__main__":
    test_index_page()
