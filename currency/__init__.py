"""
汇率查询模块
提供统一的汇率查询接口
"""

from .main import (
    get_rate,
    get_rate_with_info,
    get_supported_currencies,
    get_supported_providers,
    validate_currency_code,
)

__version__ = "1.0.0"
__author__ = "openhands-hotaru"
__email__ = "openhands@all-hands.dev"

__all__ = [
    'get_rate',
    'get_rate_with_info',
    'get_supported_currencies',
    'get_supported_providers',
    'validate_currency_code',
]