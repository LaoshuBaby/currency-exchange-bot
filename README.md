# Currency汇率查询模块

一个简洁统一的汇率查询Python模块，支持多个汇率API提供者。

## 模块结构
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

## 核心功能
- **统一接口**: 提供简单的`get_rate()`函数
- **多提供者支持**: 4个不同的汇率查询提供者
- **货币代码验证**: 支持24种常见货币
- **错误处理**: 完善的异常处理和验证

## 使用方法
```python
from currency import get_rate

# 基本使用（默认提供者）
result = get_rate("JPY", "CNY", 100)  # 100日元兑人民币

# 指定提供者
result = get_rate("USD", "EUR", 1, provider="frankfurter")
```

## 支持的提供者
1. **exchangerate_api** (默认) - ExchangeRate-API
2. **frankfurter** - Frankfurter API
3. **openexchangerates** - Open Exchange Rates
4. **google_finance** - Google财经页面

## 支持的货币
- **主要货币**: USD, EUR, GBP, JPY, CNY, HKD, KRW, AUD, CAD, SGD
- **其他货币**: CHF, INR, RUB, BRL, MXN, IDR, THB, VND, MYR, PHP
- **加密货币**: BTC, ETH
- **贵金属**: XAU (黄金), XAG (白银)