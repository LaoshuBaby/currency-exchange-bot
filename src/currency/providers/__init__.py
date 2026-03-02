"""
汇率查询提供者模块
"""

from .base_provider import BaseProvider
from .exchangerate_api import ExchangeRateAPIProvider
from .frankfurter import FrankfurterProvider
from .openexchangerates import OpenExchangeRatesProvider
from .google_finance import GoogleFinanceProvider

# 提供者映射表
PROVIDERS = {
    "exchangerate_api": ExchangeRateAPIProvider,
    "frankfurter": FrankfurterProvider,
    "openexchangerates": OpenExchangeRatesProvider,
    "google_finance": GoogleFinanceProvider,
}

def get_provider(provider_name: str):
    """获取指定名称的提供者实例"""
    provider_class = PROVIDERS.get(provider_name)
    if not provider_class:
        raise ValueError(f"未知的提供者: {provider_name}")
    return provider_class()