#!/usr/bin/env python3
"""
Currency Exchange Bot 使用示例
"""

from currency import get_rate, get_supported_currencies, get_supported_providers

def main():
    print("=" * 60)
    print("Currency Exchange Bot 使用示例")
    print("=" * 60)
    
    # 1. 显示支持的货币
    print("\n📊 支持的货币代码:")
    currencies = get_supported_currencies()
    for i, currency in enumerate(currencies, 1):
        print(f"{currency:4}", end=" ")
        if i % 8 == 0:
            print()
    print("\n")
    
    # 2. 显示支持的提供者
    print("🔧 支持的汇率提供者:")
    providers = get_supported_providers()
    for provider in providers:
        print(f"  • {provider}")
    print()
    
    # 3. 示例查询
    print("💱 汇率查询示例:")
    print("-" * 40)
    
    # 示例1: 100日元兑人民币
    try:
        result = get_rate("JPY", "CNY", 100)
        print(f"1. 100日元兑人民币: {result:.2f} CNY")
    except Exception as e:
        print(f"1. 查询失败: {e}")
    
    # 示例2: 1美元兑欧元
    try:
        result = get_rate("USD", "EUR", 1, provider="frankfurter")
        print(f"2. 1美元兑欧元: {result:.4f} EUR")
    except Exception as e:
        print(f"2. 查询失败: {e}")
    
    # 示例3: 1000韩元兑日元
    try:
        result = get_rate("KRW", "JPY", 1000, provider="exchangerate_api")
        print(f"3. 1000韩元兑日元: {result:.2f} JPY")
    except Exception as e:
        print(f"3. 查询失败: {e}")
    
    # 示例4: 1比特币兑美元
    try:
        result = get_rate("BTC", "USD", 1, provider="google_finance")
        print(f"4. 1比特币兑美元: {result:.2f} USD")
    except Exception as e:
        print(f"4. 查询失败: {e}")
    
    print("\n" + "=" * 60)
    print("💡 提示:")
    print("• 使用不同的provider可能会有不同的汇率结果")
    print("• 某些provider可能需要API密钥")
    print("• 实际使用时请确保网络连接正常")
    print("=" * 60)

if __name__ == "__main__":
    main()