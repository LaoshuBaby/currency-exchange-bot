"""
汇率查询提供者基类
提供统一的日志记录功能
"""

import abc
from typing import Optional
from ..logging_utils import get_logger, log_http_request, log_http_response, log_exchange_request, log_exchange_result

class BaseProvider(abc.ABC):
    """汇率查询提供者基类"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.logger = get_logger(f"currency.provider.{self.name}")
    
    @abc.abstractmethod
    def _get_rate_impl(self, from_currency: str, to_currency: str, amount: float = 1.0) -> Optional[float]:
        """
        具体的汇率查询实现（由子类实现）
        
        Args:
            from_currency: 来源货币代码
            to_currency: 目标货币代码
            amount: 来源货币金额
            
        Returns:
            换算后的目标货币金额，失败返回None
        """
        pass
    
    def get_rate(self, from_currency: str, to_currency: str, amount: float = 1.0) -> Optional[float]:
        """
        获取汇率（带日志记录）
        
        Args:
            from_currency: 来源货币代码
            to_currency: 目标货币代码
            amount: 来源货币金额
            
        Returns:
            换算后的目标货币金额，失败返回None
        """
        # 记录查询请求
        log_exchange_request(
            self.logger,
            from_currency,
            to_currency,
            amount,
            self.name
        )
        
        try:
            # 调用具体实现
            result = self._get_rate_impl(from_currency, to_currency, amount)
            
            # 记录查询结果
            log_exchange_result(
                self.logger,
                from_currency,
                to_currency,
                amount,
                result,
                self.name,
                None if result is not None else f"{self.name} 查询失败"
            )
            
            return result
            
        except Exception as e:
            # 记录异常
            log_exchange_result(
                self.logger,
                from_currency,
                to_currency,
                amount,
                None,
                self.name,
                str(e)
            )
            return None
    
    def log_http_request(self, method: str, url: str, headers=None, params=None, data=None):
        """记录HTTP请求"""
        log_http_request(self.logger, method, url, headers, params, data)
    
    def log_http_response(self, method: str, url: str, status_code: int, response_text=None, response_json=None, error=None):
        """记录HTTP响应"""
        log_http_response(self.logger, method, url, status_code, response_text, response_json, error)