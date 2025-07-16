#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试所有路由是否正常工作
"""

import requests
import sys

def test_route(url, description, expect_redirect=False):
    """测试单个路由"""
    try:
        response = requests.get(url, allow_redirects=False)
        
        if expect_redirect:
            if response.status_code in [302, 301]:
                print(f"✓ {description} - 重定向正常 ({response.status_code})")
                return True
            else:
                print(f"✗ {description} - 期望重定向但得到 {response.status_code}")
                return False
        else:
            if response.status_code == 200:
                print(f"✓ {description} - 正常 (200)")
                return True
            else:
                print(f"✗ {description} - 错误 ({response.status_code})")
                return False
                
    except Exception as e:
        print(f"✗ {description} - 连接失败: {e}")
        return False

def main():
    base_url = "http://127.0.0.1:5000"
    
    print("=== 仪器管理系统路由测试 ===\n")
    
    # 测试公开路由
    print("📋 测试公开路由:")
    public_routes = [
        ("/", "登录页面"),
    ]
    
    public_success = 0
    for route, desc in public_routes:
        if test_route(f"{base_url}{route}", desc):
            public_success += 1
    
    print(f"\n公开路由测试结果: {public_success}/{len(public_routes)} 通过\n")
    
    # 测试需要登录的路由（应该重定向到登录页）
    print("🔒 测试需要登录的路由（应该重定向）:")
    protected_routes = [
        ("/index", "主页"),
        ("/search_instrument", "仪器查询"),
        ("/new_store", "新仪器登记"),
        ("/storage", "设备入库"),
        ("/borrow", "仪器借用"),
        ("/return", "归还仪器"),
        ("/search_student", "用户查询"),
        ("/change_password", "修改密码"),
        ("/change_info", "修改信息"),
        ("/user/admin", "用户信息"),
        ("/logout", "登出"),
    ]
    
    protected_success = 0
    for route, desc in protected_routes:
        if test_route(f"{base_url}{route}", desc, expect_redirect=True):
            protected_success += 1
    
    print(f"\n受保护路由测试结果: {protected_success}/{len(protected_routes)} 通过\n")
    
    # 测试API路由
    print("🔌 测试API路由:")
    api_routes = [
        ("/api/statistics", "统计数据API"),
        ("/api/trend-data", "趋势数据API"),
        ("/api/category-data", "类别数据API"),
        ("/api/usage-data", "使用率数据API"),
        ("/api/user-activity-data", "用户活跃度API"),
    ]
    
    api_success = 0
    for route, desc in api_routes:
        if test_route(f"{base_url}{route}", desc, expect_redirect=True):  # API也需要登录
            api_success += 1
    
    print(f"\nAPI路由测试结果: {api_success}/{len(api_routes)} 通过\n")
    
    # 总结
    total_routes = len(public_routes) + len(protected_routes) + len(api_routes)
    total_success = public_success + protected_success + api_success
    
    print("=" * 50)
    print(f"总体测试结果: {total_success}/{total_routes} 路由正常")
    
    if total_success == total_routes:
        print("🎉 所有路由测试通过！系统运行正常。")
        return 0
    else:
        print("⚠️  部分路由测试失败，请检查系统配置。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
