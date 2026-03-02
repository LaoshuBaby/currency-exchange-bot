#!/usr/bin/env python3
"""
汇率查询脚本 - 通过Google搜索获取100日元兑人民币的汇率
"""

import requests
import re
import json
import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time

def get_google_search_results(query, num_results=10):
    """
    通过Google搜索获取结果
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # 编码查询字符串
    encoded_query = quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"搜索请求失败: {e}")
        return None

def extract_exchange_rate_from_html(html_content):
    """
    从HTML内容中提取汇率信息
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 方法1: 查找包含汇率信息的div
    exchange_patterns = [
        r'1\s*日元\s*[=≈]\s*[\d.,]+\s*人民币',
        r'1\s*JPY\s*[=≈]\s*[\d.,]+\s*CNY',
        r'100\s*日元\s*[=≈]\s*[\d.,]+\s*人民币',
        r'100\s*JPY\s*[=≈]\s*[\d.,]+\s*CNY',
        r'[\d.,]+\s*人民币\s*[=≈]\s*1\s*日元',
        r'[\d.,]+\s*CNY\s*[=≈]\s*1\s*JPY',
    ]
    
    # 查找所有文本内容
    all_text = soup.get_text()
    
    for pattern in exchange_patterns:
        matches = re.findall(pattern, all_text, re.IGNORECASE)
        if matches:
            return matches[0]
    
    # 方法2: 查找包含数字和货币单位的span/div
    for element in soup.find_all(['span', 'div', 'td']):
        text = element.get_text().strip()
        if ('日元' in text or 'JPY' in text) and ('人民币' in text or 'CNY' in text or '元' in text):
            # 检查是否包含数字
            if re.search(r'\d', text):
                return text
    
    # 方法3: 查找表格数据
    tables = soup.find_all('table')
    for table in tables:
        table_text = table.get_text()
        if ('日元' in table_text or 'JPY' in table_text) and ('人民币' in table_text or 'CNY' in text):
            return table_text[:200]  # 返回前200个字符
    
    return None

def parse_exchange_rate(rate_text):
    """
    解析汇率文本，提取数值
    """
    if not rate_text:
        return None
    
    # 查找所有数字（包括小数点和逗号）
    numbers = re.findall(r'[\d,]+\.?\d*', rate_text)
    
    if not numbers:
        return None
    
    # 清理数字（移除逗号）
    cleaned_numbers = []
    for num in numbers:
        cleaned = num.replace(',', '')
        try:
            cleaned_numbers.append(float(cleaned))
        except ValueError:
            continue
    
    if not cleaned_numbers:
        return None
    
    # 根据上下文判断哪个是汇率值
    # 通常汇率是小于1的小数（1日元 ≈ 0.046人民币）
    for num in cleaned_numbers:
        if 0.001 < num < 1.0:
            return num
    
    # 如果没有找到小数，返回第一个数字
    return cleaned_numbers[0]

def get_jpy_to_cny_rate():
    """
    主函数：获取日元兑人民币汇率
    """
    print("=" * 60)
    print("汇率查询工具 - 100日元兑人民币")
    print("=" * 60)
    
    # 尝试不同的搜索查询
    queries = [
        "100日元兑人民币汇率",
        "JPY to CNY exchange rate",
        "100日元等于多少人民币",
        "日元人民币汇率",
        "100 JPY to CNY"
    ]
    
    all_results = []
    
    for i, query in enumerate(queries, 1):
        print(f"\n尝试查询 {i}/{len(queries)}: {query}")
        
        html_content = get_google_search_results(query)
        if not html_content:
            print(f"  查询失败: {query}")
            continue
        
        rate_text = extract_exchange_rate_from_html(html_content)
        
        if rate_text:
            print(f"  找到汇率信息: {rate_text[:100]}...")
            
            rate_value = parse_exchange_rate(rate_text)
            if rate_value:
                # 如果是1日元的汇率，计算100日元的汇率
                if rate_value < 1:
                    rate_100_jpy = rate_value * 100
                else:
                    # 如果已经是100日元的汇率
                    rate_100_jpy = rate_value
                
                result = {
                    'query': query,
                    'rate_text': rate_text[:200],
                    'rate_value': rate_value,
                    'rate_100_jpy': rate_100_jpy,
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                all_results.append(result)
                
                print(f"  解析结果: 1日元 ≈ {rate_value:.6f} 人民币")
                print(f"           100日元 ≈ {rate_100_jpy:.4f} 人民币")
            else:
                print(f"  无法解析数值: {rate_text[:100]}...")
        else:
            print("  未找到汇率信息")
        
        # 避免请求过快
        if i < len(queries):
            time.sleep(2)
    
    return all_results

def save_results_to_file(results, filename="exchange_rate_results.json"):
    """
    将结果保存到JSON文件
    """
    if not results:
        print("\n未获取到有效结果，不保存文件")
        return
    
    output = {
        'query_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
        'timezone': 'Asia/Tokyo (JST)',
        'results': results,
        'summary': {
            'average_rate_100_jpy': sum(r['rate_100_jpy'] for r in results) / len(results),
            'min_rate_100_jpy': min(r['rate_100_jpy'] for r in results),
            'max_rate_100_jpy': max(r['rate_100_jpy'] for r in results),
            'num_results': len(results)
        }
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {filename}")
    print(f"平均汇率: 100日元 ≈ {output['summary']['average_rate_100_jpy']:.4f} 人民币")
    print(f"汇率范围: {output['summary']['min_rate_100_jpy']:.4f} - {output['summary']['max_rate_100_jpy']:.4f} 人民币")

def main():
    """
    主程序入口
    """
    print(f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"系统时区: Asia/Tokyo (JST)")
    
    try:
        results = get_jpy_to_cny_rate()
        
        if results:
            save_results_to_file(results)
            
            # 显示最佳结果
            print("\n" + "=" * 60)
            print("最佳估计汇率:")
            avg_rate = sum(r['rate_100_jpy'] for r in results) / len(results)
            print(f"100日元 ≈ {avg_rate:.4f} 人民币")
            print(f"1日元 ≈ {avg_rate/100:.6f} 人民币")
            print("=" * 60)
        else:
            print("\n未能获取到汇率信息，请检查网络连接或稍后重试")
            
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()