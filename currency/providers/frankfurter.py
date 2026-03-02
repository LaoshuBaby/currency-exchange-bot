"""
Frankfurter 提供者
API文档: https://www.frankfurter.app/docs/
"""

import requests
from typing import Optional

class FrankfurterProvider:
    """Frankfurter 汇率查询提供者"""
    
    def __init__(self):
        self.name = "Frankfurter"
        self.base_url = "https://api.frankfurter.app/latest"
    
    def get_rate(self, from_currency: str, to_currency: str, amount: float = 1.0) -> Optional[float]:
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
            url = f"{self.base_url}?from={from_currency.upper()}&to={to_currency.upper()}"
            
            # 发送请求
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # 解析响应
            data = response.json()
            
            # 获取汇率
            rate = data['rates'].get(to_currency.upper())
            if rate is None:
                return None
            
            # 计算金额
            return amount * rate
            
        except Exception as e:
            print(f"[{self.name}] 查询失败: {e}")
            return None