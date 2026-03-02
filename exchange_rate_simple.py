#!/usr/bin/env python3
"""
简单汇率查询脚本 - 使用公开API获取日元兑人民币汇率
"""

import requests
import json
import datetime
import time

def get_exchange_rate_from_api():
    """
    从公开API获取汇率数据
    """
    apis = [
        {
            'name': 'ExchangeRate-API',
            'url': 'https://api.exchangerate-api.com/v4/latest/JPY',
            'parser': lambda data: data['rates']['CNY']
        },
        {
            'name': 'Frankfurter',
            'url': 'https://api.frankfurter.app/latest?from=JPY&to=CNY',
            'parser': lambda data: data['rates']['CNY']
        },
        {
            'name': 'Open Exchange Rates',
            'url': 'https://open.er-api.com/v6/latest/JPY',
            'parser': lambda data: data['rates']['CNY']
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for api in apis:
        print(f"\n尝试从 {api['name']} 获取汇率...")
        try:
            response = requests.get(api['url'], headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            rate = api['parser'](data)
            print(f"  成功获取汇率: 1日元 = {rate:.6f} 人民币")
            return rate
            
        except Exception as e:
            print(f"  {api['name']} API请求失败: {e}")
            time.sleep(1)
    
    return None

def get_exchange_rate_from_google_finance():
    """
    尝试从Google财经获取汇率（备用方法）
    """
    url = "https://www.google.com/finance/quote/JPY-CNY"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        print("\n尝试从Google财经获取汇率...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 简单解析HTML查找汇率
        import re
        html = response.text
        
        # 查找汇率模式
        patterns = [
            r'data-last-price="([\d.]+)"',
            r'"JPYCNY":{"l":"([\d.]+)"',
            r'1 JPY = ([\d.]+) CNY',
            r'日元/人民币.*?([\d.]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    rate = float(matches[0])
                    print(f"  从Google财经获取汇率: 1日元 = {rate:.6f} 人民币")
                    return rate
                except ValueError:
                    continue
        
        print("  无法从Google财经页面解析汇率")
        return None
        
    except Exception as e:
        print(f"  Google财经请求失败: {e}")
        return None

def calculate_100_jpy_rate(jpy_to_cny_rate):
    """
    计算100日元兑人民币的汇率
    """
    if jpy_to_cny_rate:
        return jpy_to_cny_rate * 100
    return None

def save_result(rate_1_jpy, rate_100_jpy, filename="exchange_rate_result.json"):
    """
    保存结果到文件
    """
    result = {
        'query_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
        'timezone': 'Asia/Tokyo (JST)',
        'exchange_rate': {
            '1_JPY_to_CNY': rate_1_jpy,
            '100_JPY_to_CNY': rate_100_jpy,
            '1_CNY_to_JPY': 1 / rate_1_jpy if rate_1_jpy else None
        },
        'source': 'API/Google Finance',
        'note': '汇率数据仅供参考，实际汇率以银行柜台成交价为准'
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {filename}")

def main():
    """
    主程序
    """
    print("=" * 60)
    print("简单汇率查询工具 - 100日元兑人民币")
    print("=" * 60)
    print(f"查询时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"系统时区: Asia/Tokyo (JST)")
    
    # 方法1: 使用API获取汇率
    rate_1_jpy = get_exchange_rate_from_api()
    
    # 方法2: 如果API失败，尝试Google财经
    if not rate_1_jpy:
        rate_1_jpy = get_exchange_rate_from_google_finance()
    
    if rate_1_jpy:
        rate_100_jpy = calculate_100_jpy_rate(rate_1_jpy)
        
        print("\n" + "=" * 60)
        print("汇率查询结果:")
        print(f"1日元 ≈ {rate_1_jpy:.6f} 人民币")
        print(f"100日元 ≈ {rate_100_jpy:.4f} 人民币")
        print(f"1人民币 ≈ {1/rate_1_jpy:.4f} 日元")
        print("=" * 60)
        
        # 保存结果
        save_result(rate_1_jpy, rate_100_jpy)
        
        # 显示更多信息
        print("\n换算示例:")
        print(f"  500日元 ≈ {500 * rate_1_jpy:.2f} 人民币")
        print(f"  1000日元 ≈ {1000 * rate_1_jpy:.2f} 人民币")
        print(f"  5000日元 ≈ {5000 * rate_1_jpy:.2f} 人民币")
        print(f"  10000日元 ≈ {10000 * rate_1_jpy:.2f} 人民币")
    else:
        print("\n未能获取汇率信息")
        print("可能的原因:")
        print("  1. 网络连接问题")
        print("  2. API服务暂时不可用")
        print("  3. 请求被限制")
        print("\n建议稍后重试或使用其他汇率查询工具")

if __name__ == "__main__":
    main()