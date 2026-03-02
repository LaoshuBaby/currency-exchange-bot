"""
ExchangeRate-API 提供者
API文档: https://www.exchangerate-api.com/docs/free
"""

import requests
from typing import Optional
from .base_provider import BaseProvider

class ExchangeRateAPIProvider(BaseProvider):
    """ExchangeRate-API 汇率查询提供者"""
    
    def __init__(self):
        super().__init__()
        self.name = "ExchangeRate-API"
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
    
    def _get_rate_impl(self, from_currency: str, to_currency: str, amount: float = 1.0) -> Optional[float]:
        """
        获取汇率
        
        Args:
            from_currency: 来源货币代码
            to_currency: 目标货币代码
            amount: 来源货币金额
            
        Returns:
            换算后的目标货币金额，失败返回None
        """
        try:
            # 构建API URL
            url = f"{self.base_url}/{from_currency.upper()}"
            
            # 记录HTTP请求
            self.log_http_request("GET", url)
            
            # 发送请求
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # 解析响应
            data = response.json()
            
            # 记录HTTP响应
            self.log_http_response("GET", url, response.status_code, response_json=data)
            
            # 获取汇率
            rate = data['rates'].get(to_currency.upper())
            if rate is None:
                return None
            
            # 计算金额
            return amount * rate
            
        except Exception as e:
            self.logger.error(f"查询失败: {e}")
            return None