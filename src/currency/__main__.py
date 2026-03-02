"""
汇率查询模块主入口
提供统一的汇率查询接口

可作为模块导入使用，也可作为命令行工具运行：
python -m currency JPY CNY 100
python -m currency --from USD --to EUR --amount 1 --provider frankfurter
python -m currency --list-currencies
python -m currency --list-providers
"""

import sys
import argparse
from typing import Optional
from .providers import get_provider

# 支持的货币代码和名称映射
CURRENCY_CODES = {
    # 主要货币
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
    
    # 其他常见货币
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
    
    # 加密货币（部分API可能支持）
    'BTC': '比特币',
    'ETH': '以太坊',
    
    # 贵金属
    'XAU': '黄金',
    'XAG': '白银',
}

# 支持的提供者列表
SUPPORTED_PROVIDERS = [
    'exchangerate_api',  # ExchangeRate-API（默认）
    'frankfurter',       # Frankfurter
    'openexchangerates', # Open Exchange Rates
    'google_finance',    # Google Finance
]

def validate_currency_code(currency_code: str) -> bool:
    """
    验证货币代码是否有效
    
    Args:
        currency_code: 货币代码
        
    Returns:
        是否有效
    """
    return currency_code.upper() in CURRENCY_CODES

def get_supported_currencies() -> dict:
    """
    获取支持的货币代码列表
    
    Returns:
        货币代码和名称的字典
    """
    return CURRENCY_CODES.copy()

def get_supported_providers() -> list:
    """
    获取支持的提供者列表
    
    Returns:
        提供者名称列表
    """
    return SUPPORTED_PROVIDERS.copy()

def get_rate(
    from_currency: str, 
    to_currency: str, 
    amount: float = 1.0, 
    provider: str = "exchangerate_api"
) -> Optional[float]:
    """
    获取汇率换算结果
    
    Args:
        from_currency: 来源货币代码（如"JPY"）
        to_currency: 目标货币代码（如"CNY"）
        amount: 来源货币金额（默认1.0）
        provider: 查询器名称（默认"exchangerate_api"）
    
    Returns:
        换算后的目标货币金额，失败返回None
        
    Raises:
        ValueError: 货币代码无效或提供者不存在
    """
    # 验证货币代码
    if not validate_currency_code(from_currency):
        raise ValueError(f"无效的来源货币代码: {from_currency}")
    
    if not validate_currency_code(to_currency):
        raise ValueError(f"无效的目标货币代码: {to_currency}")
    
    # 验证金额
    if amount <= 0:
        raise ValueError(f"金额必须大于0: {amount}")
    
    # 获取提供者实例
    try:
        provider_instance = get_provider(provider)
    except ValueError as e:
        raise ValueError(f"无效的提供者: {provider}。支持的提供者: {', '.join(SUPPORTED_PROVIDERS)}")
    
    # 查询汇率
    result = provider_instance.get_rate(from_currency, to_currency, amount)
    
    return result

def get_rate_with_info(
    from_currency: str, 
    to_currency: str, 
    amount: float = 1.0, 
    provider: str = "exchangerate_api"
) -> dict:
    """
    获取汇率换算结果（包含详细信息）
    
    Args:
        from_currency: 来源货币代码
        to_currency: 目标货币代码
        amount: 来源货币金额
        provider: 查询器名称
        
    Returns:
        包含详细信息的字典，格式:
        {
            'success': bool,
            'from_currency': str,
            'to_currency': str,
            'amount': float,
            'result': float or None,
            'provider': str,
            'error': str or None
        }
    """
    try:
        result = get_rate(from_currency, to_currency, amount, provider)
        
        return {
            'success': result is not None,
            'from_currency': from_currency.upper(),
            'to_currency': to_currency.upper(),
            'amount': amount,
            'result': result,
            'provider': provider,
            'error': None if result is not None else f"{provider} 查询失败"
        }
    except Exception as e:
        return {
            'success': False,
            'from_currency': from_currency.upper(),
            'to_currency': to_currency.upper(),
            'amount': amount,
            'result': None,
            'provider': provider,
            'error': str(e)
        }

def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description='汇率查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s JPY CNY 100                    # 查询100日元兑人民币
  %(prog)s --from USD --to EUR --amount 1 # 查询1美元兑欧元
  %(prog)s --list-currencies              # 列出支持的货币
  %(prog)s --list-providers               # 列出支持的提供者
  %(prog)s --help                         # 显示帮助信息
        """
    )
    
    # 位置参数（简化用法）
    parser.add_argument(
        'args', nargs='*',
        help='简化用法: [from_currency] [to_currency] [amount]'
    )
    
    # 选项参数
    parser.add_argument(
        '--from', '-f', dest='from_currency',
        help='来源货币代码 (如: JPY)'
    )
    parser.add_argument(
        '--to', '-t', dest='to_currency',
        help='目标货币代码 (如: CNY)'
    )
    parser.add_argument(
        '--amount', '-a', type=float, default=1.0,
        help='来源货币金额 (默认: 1.0)'
    )
    parser.add_argument(
        '--provider', '-p', default='exchangerate_api',
        help='汇率提供者 (默认: exchangerate_api)'
    )
    parser.add_argument(
        '--list-currencies', '-lc', action='store_true',
        help='列出支持的货币代码'
    )
    parser.add_argument(
        '--list-providers', '-lp', action='store_true',
        help='列出支持的提供者'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='显示详细信息'
    )
    
    args = parser.parse_args()
    
    # 处理列表显示
    if args.list_currencies:
        print("📊 支持的货币代码:")
        currencies = get_supported_currencies()
        for i, (code, name) in enumerate(currencies.items(), 1):
            print(f"  {code:4} - {name}")
            if i % 5 == 0:
                print()
        return 0
    
    if args.list_providers:
        print("🔧 支持的汇率提供者:")
        providers = get_supported_providers()
        for provider in providers:
            print(f"  • {provider}")
        return 0
    
    # 解析参数
    from_currency = args.from_currency
    to_currency = args.to_currency
    
    # 如果使用简化位置参数
    if args.args:
        if len(args.args) >= 2:
            from_currency = args.args[0]
            to_currency = args.args[1]
        if len(args.args) >= 3:
            try:
                args.amount = float(args.args[2])
            except ValueError:
                print(f"❌ 错误: 金额参数无效: {args.args[2]}")
                return 1
    
    # 验证必要参数
    if not from_currency or not to_currency:
        print("❌ 错误: 必须指定来源货币和目标货币")
        print("   使用 --from 和 --to 选项，或使用简化格式: JPY CNY [amount]")
        return 1
    
    # 执行查询
    try:
        result = get_rate(from_currency, to_currency, args.amount, args.provider)
        
        if result is None:
            print(f"❌ 查询失败: {from_currency} → {to_currency}")
            return 1
        
        # 显示结果
        from_name = CURRENCY_CODES.get(from_currency.upper(), from_currency)
        to_name = CURRENCY_CODES.get(to_currency.upper(), to_currency)
        
        print(f"💱 汇率查询结果:")
        print(f"   {args.amount:.2f} {from_currency} ({from_name})")
        print(f"   = {result:.4f} {to_currency} ({to_name})")
        
        if args.verbose:
            print(f"   提供者: {args.provider}")
            print(f"   汇率: 1 {from_currency} = {result/args.amount:.6f} {to_currency}")
        
        return 0
        
    except ValueError as e:
        print(f"❌ 错误: {e}")
        return 1
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())