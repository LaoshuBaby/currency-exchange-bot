"""
汇率查询模块主入口
提供统一的汇率查询接口
"""

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