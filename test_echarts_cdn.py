#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

def test_echarts_cdn():
    """测试ECharts CDN是否可用"""
    print("=== ECharts CDN测试 ===\n")
    
    cdn_url = "https://cdn.jsdelivr.net/npm/echarts@5.4.0/dist/echarts.min.js"
    
    try:
        response = requests.get(cdn_url, timeout=10)
        print(f"CDN状态码: {response.status_code}")
        print(f"内容长度: {len(response.text)} 字符")
        
        if response.status_code == 200 and len(response.text) > 1000:
            print("✅ ECharts CDN可用")
            return True
        else:
            print("❌ ECharts CDN不可用")
            return False
            
    except Exception as e:
        print(f"❌ CDN测试异常: {e}")
        return False

if __name__ == "__main__":
    test_echarts_cdn()
