#!/usr/bin/env python3
"""
多货币汇率查询脚本 - 支持任意货币对查询
"""

import requests
import json
import datetime
import time
import sys

def get_exchange_rate_from_api(from_currency, to_currency):
    """
    从公开API获取任意货币对的汇率
    """
    apis = [
        {
            'name': 'ExchangeRate-API',
            'url': f'https://api.exchangerate-api.com/v4/latest/{from_currency}',
            'parser': lambda data, to_curr: data['rates'].get(to_curr)
        },
        {
            'name': 'Frankfurter',
            'url': f'https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}',
            'parser': lambda data, to_curr: data['rates'].get(to_curr)
        },
        {
            'name': 'Open Exchange Rates',
            'url': f'https://open.er-api.com/v6/latest/{from_currency}',
            'parser': lambda data, to_curr: data['rates'].get(to_curr)
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for api in apis:
        print(f"\n尝试从 {api['name']} 获取 {from_currency}->{to_currency} 汇率...")
        try:
            response = requests.get(api['url'], headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            rate = api['parser'](data, to_currency)
            if rate:
                print(f"  成功获取汇率: 1 {from_currency} = {rate:.6f} {to_currency}")
                return rate
            else:
                print(f"  API未返回目标货币 {to_currency} 的汇率")
                
        except Exception as e:
            print(f"  {api['name']} API请求失败: {e}")
            time.sleep(1)
    
    return None

def get_available_currencies():
    """
    获取支持的货币列表
    """
    common_currencies = {
        'USD': '美元',
        'EUR': '欧元',
        'GBP': '英镑',
        'JPY': '日元',
        'CNY': '人民币',
        'HKD': '港币',
        'KRW': '韩元',
        'AUD': '澳元',
        'CAD': '加元',
        'SGD': '新加坡元',
        'CHF': '瑞士法郎',
        'INR': '印度卢比',
        'RUB': '俄罗斯卢布',
        'BRL': '巴西雷亚尔',
        'MXN': '墨西哥比索',
        'IDR': '印尼盾',
        'THB': '泰铢',
        'VND': '越南盾',
        'MYR': '马来西亚林吉特',
        'PHP': '菲律宾比索',
    }
    return common_currencies

def calculate_amounts(rate, from_currency, to_currency):
    """
    计算常见金额的换算
    """
    amounts = [1, 10, 50, 100, 500, 1000, 5000, 10000]
    
    print(f"\n换算示例:")
    for amount in amounts:
        converted = amount * rate
        print(f"  {amount:6,d} {from_currency} ≈ {converted:10.2f} {to_currency}")
    
    # 反向换算
    if rate > 0:
        reverse_rate = 1 / rate
        print(f"\n反向换算 (1 {to_currency} ≈ {reverse_rate:.4f} {from_currency}):")
        for amount in [1, 10, 50, 100]:
            converted = amount * reverse_rate
            print(f"  {amount:6,d} {to_currency} ≈ {converted:10.2f} {from_currency}")

def save_result(from_currency, to_currency, rate, filename=None):
    """
    保存结果到文件
    """
    if not filename:
        filename = f"exchange_rate_{from_currency}_{to_currency}.json"
    
    result = {
        'query_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
        'timezone': 'Asia/Tokyo (JST)',
        'exchange_rate': {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'rate': rate,
            'reverse_rate': 1 / rate if rate else None
        },
        'source': 'Multiple APIs',
        'note': '汇率数据仅供参考，实际汇率以银行柜台成交价为准'
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {filename}")
    return filename

def main():
    """
    主程序
    """
    print("=" * 60)
    print("多货币汇率查询工具")
    print("=" * 60)
    print(f"查询时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"系统时区: Asia/Tokyo (JST)")
    
    # 获取支持的货币列表
    currencies = get_available_currencies()
    
    # 显示常用货币
    print("\n常用货币代码:")
    for code, name in list(currencies.items())[:10]:  # 只显示前10个
        print(f"  {code}: {name}")
    print("  ... (共{}种货币)".format(len(currencies)))
    
    # 获取用户输入或使用默认值
    if len(sys.argv) >= 3:
        from_currency = sys.argv[1].upper()
        to_currency = sys.argv[2].upper()
        amount = float(sys.argv[3]) if len(sys.argv) >= 4 else 100
    else:
        # 使用默认值：日元兑人民币
        from_currency = 'JPY'
        to_currency = 'CNY'
        amount = 100
    
    print(f"\n查询汇率: {from_currency} -> {to_currency}")
    
    # 获取汇率
    rate = get_exchange_rate_from_api(from_currency, to_currency)
    
    if rate:
        print("\n" + "=" * 60)
        print("汇率查询结果:")
        print(f"1 {from_currency} ≈ {rate:.6f} {to_currency}")
        print(f"{amount} {from_currency} ≈ {amount * rate:.4f} {to_currency}")
        
        if rate > 0:
            print(f"1 {to_currency} ≈ {1/rate:.4f} {from_currency}")
        print("=" * 60)
        
        # 计算换算示例
        calculate_amounts(rate, from_currency, to_currency)
        
        # 保存结果
        save_result(from_currency, to_currency, rate)
        
    else:
        print(f"\n未能获取 {from_currency} 到 {to_currency} 的汇率信息")
        print("可能的原因:")
        print("  1. 货币代码不正确")
        print("  2. API服务暂时不可用")
        print("  3. 网络连接问题")
        print("\n支持的货币代码示例:")
        for code, name in list(currencies.items())[:15]:
            print(f"  {code} ({name})")

def show_usage():
    """
    显示使用说明
    """
    print("使用说明:")
    print("  python3 exchange_rate_multi.py [来源货币] [目标货币] [金额]")
    print()
    print("示例:")
    print("  python3 exchange_rate_multi.py JPY CNY 100    # 100日元兑人民币")
    print("  python3 exchange_rate_multi.py USD CNY 1      # 1美元兑人民币")
    print("  python3 exchange_rate_multi.py EUR USD 100    # 100欧元兑美元")
    print("  python3 exchange_rate_multi.py               # 使用默认值(JPY->CNY)")
    print()
    print("常用货币代码:")
    currencies = get_available_currencies()
    for code, name in currencies.items():
        print(f"  {code}: {name}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_usage()
    else:
        main()