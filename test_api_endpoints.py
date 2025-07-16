#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup
import json

def test_api_endpoints():
    """测试所有API接口"""
    session = requests.Session()
    base_url = "http://127.0.0.1:5000"
    
    print("=== API接口测试 ===\n")
    
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
    
    # 2. 测试所有API接口
    print("\n2. 测试API接口...")
    api_endpoints = [
        ("/api/statistics", "系统统计数据"),
        ("/api/trend-data", "借还趋势数据"),
        ("/api/category-data", "仪器类别分布"),
        ("/api/usage-data", "设备使用率排行"),
        ("/api/user-activity-data", "用户活跃度数据"),
    ]
    
    success_count = 0
    for endpoint, description in api_endpoints:
        try:
            response = session.get(f"{base_url}{endpoint}")
            print(f"\n{description} ({endpoint}):")
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'error' in data:
                        print(f"  ❌ API返回错误: {data['error']}")
                    else:
                        print(f"  ✅ API正常，数据类型: {type(data)}")
                        if isinstance(data, dict):
                            print(f"  数据键: {list(data.keys())}")
                        elif isinstance(data, list):
                            print(f"  数据长度: {len(data)}")
                        success_count += 1
                except json.JSONDecodeError:
                    print(f"  ❌ 响应不是有效的JSON")
                    print(f"  响应内容: {response.text[:100]}...")
            else:
                print(f"  ❌ API访问失败")
                print(f"  响应内容: {response.text[:100]}...")
                
        except Exception as e:
            print(f"  ❌ API测试异常: {e}")
    
    print(f"\n测试结果: {success_count}/{len(api_endpoints)} 个API正常")
    
    if success_count == len(api_endpoints):
        print("🎉 所有API接口都正常工作！")
        return True
    else:
        print("⚠️  部分API接口存在问题")
        return False

if __name__ == "__main__":
    test_api_endpoints()
