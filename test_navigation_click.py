#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup
import re

def test_navigation_links():
    """测试导航链接"""
    session = requests.Session()
    base_url = "http://127.0.0.1:5000"
    
    print("=== 导航链接测试 ===\n")
    
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
        
        login_response = session.post(f"{base_url}/", data=login_data, allow_redirects=True)
        if login_response.status_code == 200 and "/index" in login_response.url:
            print("✅ 登录成功，已在index页面")
        else:
            print("❌ 登录失败")
            return False
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return False
    
    # 2. 解析当前页面的导航链接
    print("\n2. 解析导航链接...")
    try:
        soup = BeautifulSoup(login_response.text, 'html.parser')
        
        # 查找所有导航链接
        nav_links = soup.find_all('a', href=True)
        
        print("找到的导航链接:")
        for link in nav_links:
            href = link.get('href')
            text = link.get_text(strip=True)
            if href and not href.startswith('javascript:') and not href.startswith('#'):
                print(f"  {text}: {href}")
        
        # 特别检查系统概览链接
        index_links = [link for link in nav_links if 'index' in link.get('href', '')]
        print(f"\n系统概览相关链接: {len(index_links)} 个")
        for link in index_links:
            print(f"  文本: '{link.get_text(strip=True)}'")
            print(f"  链接: '{link.get('href')}'")
            print(f"  父元素: {link.parent.name}")
            
    except Exception as e:
        print(f"❌ 解析导航异常: {e}")
        return False
    
    # 3. 测试从其他页面跳转到系统概览
    print("\n3. 测试跳转到系统概览...")
    
    # 先跳转到其他页面
    try:
        other_page = session.get(f"{base_url}/new_store")
        if other_page.status_code == 200:
            print("✅ 成功跳转到新仪器登记页面")
            
            # 再跳转回系统概览
            index_page = session.get(f"{base_url}/index")
            if index_page.status_code == 200:
                print("✅ 成功从其他页面跳转回系统概览")
                
                # 检查导航状态
                soup = BeautifulSoup(index_page.text, 'html.parser')
                expanded_menu = soup.find('li', class_='layui-nav-item layui-nav-itemed')
                selected_item = soup.find('dd', class_='layui-this')
                
                if expanded_menu and selected_item:
                    print("✅ 导航状态正确：菜单已展开，项目已选中")
                else:
                    print("❌ 导航状态不正确")
                    print(f"  展开菜单: {expanded_menu is not None}")
                    print(f"  选中项目: {selected_item is not None}")
            else:
                print(f"❌ 跳转回系统概览失败: {index_page.status_code}")
        else:
            print(f"❌ 跳转到其他页面失败: {other_page.status_code}")
            
    except Exception as e:
        print(f"❌ 跳转测试异常: {e}")
        return False
    
    print("\n🎉 导航链接测试完成")
    return True

if __name__ == "__main__":
    test_navigation_links()
