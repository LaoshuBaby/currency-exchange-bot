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
from currency import get_rate

# 基本使用（默认提供者）
result = get_rate("JPY", "CNY", 100)  # 100日元兑人民币

# 指定提供者
result = get_rate("USD", "EUR", 1, provider="frankfurter")
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
  - `/exchange [金额] [来源货币] [目标货币]` - 货币兑换查询
      - 格式1: `/exchange 100 JPY CNY` (查询100日元兑人民币)
      - 格式2: `/exchange JPY CNY` (查询1日元兑人民币)
  - `/time` - 显示东京时间
  - `/about` - 关于机器人

### 3. `BOT_SETUP.md`
- **功能**: 详细的Telegram机器人设置指南
- **内容**: 创建机器人、配置Token、运行测试、故障排除