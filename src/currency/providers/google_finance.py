"""
Google Finance 提供者
通过Google财经页面获取汇率
"""

import requests
import re
from typing import Optional

class GoogleFinanceProvider:
    """Google Finance 汇率查询提供者"""
    
    def __init__(self):
        self.name = "Google Finance"
        self.base_url = "https://www.google.com/finance/quote"
    
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
            # 构建Google财经URL
            url = f"{self.base_url}/{from_currency.upper()}-{to_currency.upper()}"
            
            # 设置请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            }
            
            # 发送请求
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 从HTML中提取汇率
            html = response.text
            
            # 尝试多种模式匹配汇率
            patterns = [
                r'data-last-price="([\d.]+)"',
                r'"l":"([\d.]+)"',
                rf'1\s*{from_currency.upper()}\s*=\s*([\d.]+)\s*{to_currency.upper()}',
                r'data-exchange-rate="([\d.]+)"',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html)
                if matches:
                    try:
                        rate = float(matches[0])
                        return amount * rate
                    except (ValueError, IndexError):
                        continue
            
            # 如果所有模式都失败，返回None
            return None
            
        except Exception as e:
            print(f"[{self.name}] 查询失败: {e}")
            return None