"""
Open Exchange Rates 提供者
API文档: https://docs.openexchangerates.org/
注意：需要API密钥，但免费版每月有1000次请求限制
"""

import requests
from typing import Optional
from .base_provider import BaseProvider

class OpenExchangeRatesProvider(BaseProvider):
    """Open Exchange Rates 汇率查询提供者"""
    
    def __init__(self):
        super().__init__()
        self.name = "Open Exchange Rates"
        self.base_url = "https://open.er-api.com/v6/latest"
        # 注意：实际使用时需要API密钥，这里使用公开端点
        # 正式使用应配置API密钥: f"{self.base_url}/{from_currency}?app_id=YOUR_APP_ID"
    
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
            # 构建API URL（使用公开端点，无需API密钥）
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
            
            # 检查API状态
            if data.get('result') != 'success':
                return None
            
            # 获取汇率
            rate = data['rates'].get(to_currency.upper())
            if rate is None:
                return None
            
            # 计算金额
            return amount * rate
            
        except Exception as e:
            self.logger.error(f"查询失败: {e}")
            return None