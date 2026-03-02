#!/usr/bin/env python3
"""
全局HTTP请求日志系统
记录所有HTTP请求和响应，包括Telegram API和汇率API
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# 全局日志文件路径
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telegram_bot.log")

class HTTPLogger:
    """全局HTTP请求日志记录器"""
    
    def __init__(self, log_file_path: str = LOG_FILE_PATH):
        self.log_file_path = log_file_path
        self._setup_logger()
    
    def _setup_logger(self):
        """设置日志记录器"""
        # 确保日志目录存在
        log_dir = os.path.dirname(self.log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 配置日志格式
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file_path, mode='a', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('http_logger')
    
    def log_request(self, 
                   method: str, 
                   url: str, 
                   headers: Optional[Dict] = None,
                   params: Optional[Dict] = None,
                   data: Optional[Any] = None,
                   source: str = "unknown"):
        """记录HTTP请求"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "http_request",
            "method": method,
            "url": url,
            "headers": headers or {},
            "params": params or {},
            "data": data if data is not None else None,
            "source": source
        }
        
        self.logger.info(f"HTTP请求: {json.dumps(log_entry, ensure_ascii=False)}")
    
    def log_response(self,
                    method: str,
                    url: str,
                    status_code: int,
                    response_text: Optional[str] = None,
                    response_json: Optional[Dict] = None,
                    source: str = "unknown"):
        """记录HTTP响应"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "http_response",
            "method": method,
            "url": url,
            "status_code": status_code,
            "response_text": response_text[:500] if response_text else None,  # 限制长度
            "response_json": response_json,
            "source": source
        }
        
        self.logger.info(f"HTTP响应: {json.dumps(log_entry, ensure_ascii=False)}")
    
    def log_error(self,
                 method: str,
                 url: str,
                 error: str,
                 source: str = "unknown"):
        """记录HTTP错误"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "http_error",
            "method": method,
            "url": url,
            "error": str(error),
            "source": source
        }
        
        self.logger.error(f"HTTP错误: {json.dumps(log_entry, ensure_ascii=False)}")
    
    def log_telegram_update(self, update_data: Dict, source: str = "telegram_bot"):
        """记录Telegram更新"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "telegram_update",
            "update_id": update_data.get('update_id'),
            "message_id": update_data.get('message', {}).get('message_id'),
            "chat_id": update_data.get('message', {}).get('chat', {}).get('id'),
            "user_id": update_data.get('message', {}).get('from', {}).get('id'),
            "text": update_data.get('message', {}).get('text'),
            "source": source
        }
        
        self.logger.info(f"Telegram更新: {json.dumps(log_entry, ensure_ascii=False)}")
    
    def log_telegram_response(self, 
                             method: str, 
                             chat_id: int,
                             text: str,
                             source: str = "telegram_bot"):
        """记录Telegram响应"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "telegram_response",
            "method": method,
            "chat_id": chat_id,
            "text": text[:200],  # 限制长度
            "source": source
        }
        
        self.logger.info(f"Telegram响应: {json.dumps(log_entry, ensure_ascii=False)}")

# 全局日志实例
global_logger = HTTPLogger()

def log_http_request(method: str, url: str, **kwargs):
    """记录HTTP请求的便捷函数"""
    global_logger.log_request(method, url, **kwargs)

def log_http_response(method: str, url: str, status_code: int, **kwargs):
    """记录HTTP响应的便捷函数"""
    global_logger.log_response(method, url, status_code, **kwargs)

def log_http_error(method: str, url: str, error: str, **kwargs):
    """记录HTTP错误的便捷函数"""
    global_logger.log_error(method, url, error, **kwargs)

def log_telegram_update(update_data: Dict, **kwargs):
    """记录Telegram更新的便捷函数"""
    global_logger.log_telegram_update(update_data, **kwargs)

def log_telegram_response(method: str, chat_id: int, text: str, **kwargs):
    """记录Telegram响应的便捷函数"""
    global_logger.log_telegram_response(method, chat_id, text, **kwargs)

if __name__ == "__main__":
    # 测试日志系统
    print(f"日志文件路径: {LOG_FILE_PATH}")
    
    # 测试记录
    log_http_request("GET", "https://api.example.com/test", source="test")
    log_http_response("GET", "https://api.example.com/test", 200, source="test")
    log_http_error("GET", "https://api.example.com/test", "Connection timeout", source="test")
    
    print("日志系统测试完成")