#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup

def test_navigation_state():
    """测试导航状态保持功能"""
    session = requests.Session()
    base_url = "http://127.0.0.1:5000"
    
    print("=== 导航状态保持测试 ===\n")
    
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
    
    # 2. 测试各个页面的导航状态
    print("\n2. 测试导航状态...")
    test_pages = [
        ("/index", "📈 系统概览", "数据分析"),
        ("/new_store", "📝 新仪器登记", "仪器管理"),
        ("/storage", "📦 设备入库", "仪器管理"),
        ("/borrow", "📤 仪器借用", "仪器管理"),
        ("/return", "📥 归还仪器", "仪器管理"),
        ("/search_student", "🔍 用户查询", "用户管理"),
    ]
    
    success_count = 0
    for path, page_name, expected_menu in test_pages:
        try:
            response = session.get(f"{base_url}{path}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 检查是否有展开的菜单项
                expanded_items = soup.find_all('li', class_='layui-nav-item layui-nav-itemed')
                
                # 检查是否有选中的菜单项
                selected_items = soup.find_all('dd', class_='layui-this')
                
                if expanded_items and selected_items:
                    print(f"✅ {page_name}: 导航状态正确 - {expected_menu}菜单已展开")
                    success_count += 1
                else:
                    print(f"❌ {page_name}: 导航状态错误")
                    print(f"   展开菜单数: {len(expanded_items)}")
                    print(f"   选中项数: {len(selected_items)}")
            else:
                print(f"❌ {page_name}: 页面访问失败 ({response.status_code})")
        except Exception as e:
            print(f"❌ {page_name}: 测试异常 - {e}")
    
    print(f"\n测试结果: {success_count}/{len(test_pages)} 个页面导航状态正确")
    
    if success_count == len(test_pages):
        print("🎉 导航状态保持功能完全正常！")
        return True
    else:
        print("⚠️  部分页面导航状态仍有问题")
        return False

if __name__ == "__main__":
    test_navigation_state()
