# Currency Exchange Bot - 货币兑换机器人

一个包含统一汇率查询模块和Telegram机器人的Python项目，支持多种货币兑换查询和实时汇率获取。

[![GitHub stars](https://img.shields.io/github/stars/LaoshuBaby/currency-exchange-bot?style=social)](https://github.com/LaoshuBaby/currency-exchange-bot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/LaoshuBaby/currency-exchange-bot?style=social)](https://github.com/LaoshuBaby/currency-exchange-bot/network)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ✨ 项目特点

- **统一汇率查询模块**: 支持4个不同的汇率API提供者
- **Telegram机器人**: 提供便捷的/exchange命令进行货币兑换查询
- **多货币支持**: 支持24种常见货币，包括主要货币、加密货币和贵金属
- **灵活的参数格式**: 支持带金额和不带金额的查询
- **完善的错误处理**: 参数验证、错误提示和友好的用户界面

## 🚀 快速开始

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/LaoshuBaby/currency-exchange-bot.git
cd currency-exchange-bot

# 安装依赖
pip install -r requirements.txt
```

### 使用Currency模块

```python
from src.currency import get_rate

# 查询100日元兑人民币
result = get_rate("JPY", "CNY", 100)
print(f"100日元 ≈ {result:.2f}人民币")

# 使用指定提供者
result = get_rate("USD", "EUR", 1, provider="frankfurter")
print(f"1美元 ≈ {result:.4f}欧元")
```

### 运行Telegram机器人

1. 在Telegram中创建机器人（通过 @BotFather）
2. 获取Bot Token
3. 配置Token：
   ```bash
   # 方法1：设置环境变量
   export TELEGRAM_BOT_TOKEN="你的token"
   
   # 方法2：直接修改src/telegram_bot.py中的BOT_TOKEN变量
   ```
4. 运行机器人：
   ```bash
   python src/telegram_bot.py
   ```

## 📱 Telegram机器人命令

### `/exchange` - 货币兑换查询
```
/exchange 100 JPY CNY    # 查询100日元兑人民币
/exchange 1 USD EUR      # 查询1美元兑欧元
/exchange 5000 KRW JPY   # 查询5000韩元兑日元
/exchange JPY CNY        # 查询1日元兑人民币（默认金额为1）
```

### 其他命令
- `/start` - 开始使用机器人
- `/help` - 显示帮助信息
- `/time` - 显示当前东京时间
- `/about` - 关于机器人

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