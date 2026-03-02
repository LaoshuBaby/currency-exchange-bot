"""
日志工具模块
提供统一的日志记录功能，记录HTTP请求和响应
"""

import os
import sys
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
import inspect

# 导入全局HTTP日志系统
try:
    from http_logger import log_http_request as global_log_http_request, log_http_response as global_log_http_response
except ImportError:
    # 如果直接导入失败，尝试相对导入
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.http_logger import log_http_request as global_log_http_request, log_http_response as global_log_http_response

# 全局日志配置
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    获取或创建日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径，如果为None则使用模块同目录下的.log文件
        
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（追加模式）
    if log_file is None:
        # 获取调用模块的文件路径，并在同目录创建.log文件
        frame = inspect.currentframe()
        try:
            # 向上追溯找到调用get_logger的模块
            while frame:
                module = inspect.getmodule(frame)
                if module and module.__name__ != __name__:
                    module_file = module.__file__
                    if module_file:
                        log_file = os.path.join(
                            os.path.dirname(module_file),
                            f"{os.path.splitext(os.path.basename(module_file))[0]}.log"
                        )
                        break
                frame = frame.f_back
        finally:
            del frame
    
    if log_file:
        # 确保目录存在
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_http_request(
    logger: logging.Logger,
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Any] = None
) -> None:
    """
    记录HTTP请求
    
    Args:
        logger: 日志记录器
        method: HTTP方法
        url: 请求URL
        headers: 请求头
        params: 查询参数
        data: 请求体数据
    """
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'type': 'http_request',
        'method': method,
        'url': url,
        'headers': headers or {},
        'params': params or {},
    }
    
    if data:
        if isinstance(data, dict):
            log_data['data'] = data
        else:
            log_data['data'] = str(data)
    
    logger.info(f"HTTP请求: {json.dumps(log_data, ensure_ascii=False)}")
    
    # 同时记录到全局HTTP日志系统
    try:
        global_log_http_request(method, url, headers=headers, params=params, data=data, source=f"currency.{logger.name}")
    except Exception as e:
        logger.warning(f"记录到全局HTTP日志失败: {e}")

def log_http_response(
    logger: logging.Logger,
    method: str,
    url: str,
    status_code: int,
    response_text: Optional[str] = None,
    response_json: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None
) -> None:
    """
    记录HTTP响应
    
    Args:
        logger: 日志记录器
        method: HTTP方法
        url: 请求URL
        status_code: 状态码
        response_text: 响应文本
        response_json: 响应JSON数据
        error: 错误信息
    """
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'type': 'http_response',
        'method': method,
        'url': url,
        'status_code': status_code,
        'error': error,
    }
    
    if response_json:
        log_data['response'] = response_json
    elif response_text:
        # 截断过长的响应文本
        if len(response_text) > 1000:
            log_data['response'] = response_text[:1000] + "...[truncated]"
        else:
            log_data['response'] = response_text
    
    logger.info(f"HTTP响应: {json.dumps(log_data, ensure_ascii=False)}")
    
    # 同时记录到全局HTTP日志系统
    try:
        global_log_http_response(method, url, status_code, response_text=response_text, response_json=response_json, source=f"currency.{logger.name}")
    except Exception as e:
        logger.warning(f"记录到全局HTTP日志失败: {e}")

def log_exchange_request(
    logger: logging.Logger,
    from_currency: str,
    to_currency: str,
    amount: float,
    provider: str
) -> None:
    """
    记录汇率查询请求
    
    Args:
        logger: 日志记录器
        from_currency: 来源货币
        to_currency: 目标货币
        amount: 金额
        provider: 提供者
    """
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'type': 'exchange_request',
        'from_currency': from_currency,
        'to_currency': to_currency,
        'amount': amount,
        'provider': provider,
    }
    
    logger.info(f"汇率查询请求: {json.dumps(log_data, ensure_ascii=False)}")

def log_exchange_result(
    logger: logging.Logger,
    from_currency: str,
    to_currency: str,
    amount: float,
    result: Optional[float],
    provider: str,
    error: Optional[str] = None
) -> None:
    """
    记录汇率查询结果
    
    Args:
        logger: 日志记录器
        from_currency: 来源货币
        to_currency: 目标货币
        amount: 金额
        result: 查询结果
        provider: 提供者
        error: 错误信息
    """
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'type': 'exchange_result',
        'from_currency': from_currency,
        'to_currency': to_currency,
        'amount': amount,
        'result': result,
        'provider': provider,
        'error': error,
        'success': result is not None and error is None
    }
    
    logger.info(f"汇率查询结果: {json.dumps(log_data, ensure_ascii=False)}")