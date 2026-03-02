# 汇率查询工具和Telegram机器人

这个项目包含一个统一的currency模块用于汇率查询，以及Telegram机器人相关文件。

## Currency模块

### 模块结构
```
currency/
├── __init__.py              # 模块初始化
├── main.py                  # 主入口文件，提供统一接口
└── providers/               # 汇率查询提供者
    ├── __init__.py          # 提供者注册
    ├── exchangerate_api.py  # ExchangeRate-API提供者
    ├── frankfurter.py       # Frankfurter提供者
    ├── openexchangerates.py # Open Exchange Rates提供者
    └── google_finance.py    # Google财经提供者
```

### 核心功能
- **统一接口**: 提供简单的`get_rate()`函数
- **多提供者支持**: 4个不同的汇率查询提供者
- **货币代码验证**: 支持24种常见货币
- **错误处理**: 完善的异常处理和验证

### 主要函数
```python
from currency import get_rate, get_rate_with_info

# 基本使用（默认提供者）
result = get_rate("JPY", "CNY", 100)  # 100日元兑人民币

# 指定提供者
result = get_rate("USD", "EUR", 1, provider="frankfurter")

# 获取详细信息
info = get_rate_with_info("GBP", "JPY", 50, provider="openexchangerates")
```

### 支持的提供者
1. **exchangerate_api** (默认) - ExchangeRate-API
2. **frankfurter** - Frankfurter API
3. **openexchangerates** - Open Exchange Rates
4. **google_finance** - Google财经页面

### 支持的货币
- **主要货币**: USD, EUR, GBP, JPY, CNY, HKD, KRW, AUD, CAD, SGD
- **其他货币**: CHF, INR, RUB, BRL, MXN, IDR, THB, VND, MYR, PHP
- **加密货币**: BTC, ETH
- **贵金属**: XAU (黄金), XAG (白银)

## Telegram机器人

### 1. `telegram_bot_simple.py`
- **功能**: 简单的Telegram机器人示例
- **特点**: 演示基本命令处理，需要配置Bot Token
- **命令**: `/start` 返回 "Hello World!"

### 2. `telegram_bot_real.py`
- **功能**: 完整功能的Telegram汇率查询机器人
- **特点**: 支持多种命令，模拟汇率数据，可扩展为真实API
- **命令**: 
  - `/start` - 开始使用机器人
  - `/help` - 显示帮助信息
  - `/rate [货币代码]` - 查询汇率
  - `/time` - 显示东京时间
  - `/about` - 关于机器人

### 3. `BOT_SETUP.md`
- **功能**: 详细的Telegram机器人设置指南
- **内容**: 创建机器人、配置Token、运行测试、故障排除

## 使用方法

### 安装依赖
```bash
pip install requests beautifulsoup4 lxml
```

### 运行脚本
```bash
# 运行简单版本（推荐）
python3 exchange_rate_simple.py

# 运行网页抓取版本
python3 exchange_rate_scraper.py
```

### 输出示例
```
============================================================
简单汇率查询工具 - 100日元兑人民币
============================================================
查询时间: 2026-03-02 21:33:27
系统时区: Asia/Tokyo (JST)

尝试从 ExchangeRate-API 获取汇率...
  成功获取汇率: 1日元 = 0.043900 人民币

============================================================
汇率查询结果:
1日元 ≈ 0.043900 人民币
100日元 ≈ 4.3900 人民币
1人民币 ≈ 22.7790 日元
============================================================

结果已保存到: exchange_rate_result.json

换算示例:
  500日元 ≈ 21.95 人民币
  1000日元 ≈ 43.90 人民币
  5000日元 ≈ 219.50 人民币
  10000日元 ≈ 439.00 人民币
```

## 生成的文件

- `exchange_rate_result.json`: 汇率查询结果（JSON格式）
- 包含查询时间、汇率数据、换算示例等信息

## 系统配置

- **时区**: 东京时间（Asia/Tokyo, JST）
- **Git用户**: openhands-hotaru
- **Python版本**: 3.12+

## 注意事项

1. 汇率数据仅供参考，实际汇率以银行柜台成交价为准
2. API服务可能有调用限制，请合理使用
3. 网页抓取版本可能受到Google反爬虫机制的影响
4. 生成的JSON文件已被添加到.gitignore中，不会提交到版本控制

## 许可证

本项目仅供学习和参考使用。