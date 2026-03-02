# Telegram 机器人设置指南

## 1. 创建Telegram机器人

### 步骤：
1. 在Telegram中搜索 **@BotFather**
2. 发送 `/newbot` 命令
3. 按照提示设置：
   - 机器人名称（显示名称）
   - 机器人用户名（必须以`bot`结尾，如`my_exchange_bot`）
4. 获取API Token（类似：`1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ`）

## 2. 配置机器人

### 方法A：直接修改代码（简单但不安全）
编辑 `src/telegram_bot.py` 文件，将第20行：
```python
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
```
改为：
```python
BOT_TOKEN = "你的实际Token"
```

### 方法B：使用环境变量（推荐）
```bash
# 临时设置（当前会话有效）
export TELEGRAM_BOT_TOKEN="你的实际Token"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export TELEGRAM_BOT_TOKEN="你的实际Token"' >> ~/.bashrc
source ~/.bashrc
```

### 方法C：使用.env文件
1. 创建 `.env` 文件：
```bash
echo 'TELEGRAM_BOT_TOKEN="你的实际Token"' > .env
```
2. 安装python-dotenv：
```bash
pip install python-dotenv
```
3. 修改代码使用dotenv：
```python
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
```

## 3. 运行机器人

### 安装依赖：
```bash
pip install python-telegram-bot
```

### 运行机器人：
```bash
# 运行机器人（需要配置Token）
python3 src/telegram_bot.py
```

## 4. 测试机器人

1. 在Telegram中搜索你的机器人用户名
2. 发送 `/start` 命令
3. 你应该收到 "Hello World!" 回复

## 5. 可用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/start` | 开始使用机器人 | `/start` |
| `/help` | 显示帮助信息 | `/help` |
| `/exchange` | 查询汇率 | `/exchange JPY CNY` |
| `/time` | 显示东京时间 | `/time` |
| `/about` | 关于机器人 | `/about` |

## 6. 支持的货币代码

- **USD** - 美元
- **EUR** - 欧元  
- **GBP** - 英镑
- **JPY** - 日元
- **CNY** - 人民币
- **HKD** - 港币
- **KRW** - 韩元
- **AUD** - 澳元
- **CAD** - 加元
- **SGD** - 新加坡元

## 7. 故障排除

### 问题1：Token无效
```
❌ 错误：未设置有效的Bot Token！
```
**解决方案**：检查Token是否正确，确保没有多余的空格。

### 问题2：无法连接
```
❌ 启动机器人失败：网络错误
```
**解决方案**：检查网络连接，确保可以访问Telegram API。

### 问题3：命令不响应
```
机器人收到消息但没有回复
```
**解决方案**：
1. 检查机器人是否正在运行
2. 查看日志输出
3. 确保使用了正确的命令格式

### 问题4：依赖错误
```
ModuleNotFoundError: No module named 'telegram'
```
**解决方案**：
```bash
pip install python-telegram-bot
```

## 8. 安全注意事项

1. **不要公开Token**：Token相当于机器人的密码，不要提交到公开仓库
2. **使用环境变量**：在生产环境中使用环境变量存储Token
3. **限制访问**：可以为机器人设置隐私模式，只允许特定用户使用
4. **定期更新**：定期检查并更新依赖库

## 9. 扩展功能

### 集成真实汇率API
修改 `src/telegram_bot.py` 中的 `get_mock_rate()` 函数，调用真实的汇率API：

```python
def get_real_rate(from_currency, to_currency):
    """调用真实汇率API"""
    try:
        # 使用currency模块的汇率查询函数
        from src.currency import get_rate
        return get_rate(from_currency, to_currency, 1.0)
    except:
        return None
```

### 添加更多命令
在 `main()` 函数中添加新的命令处理器：
```python
application.add_handler(CommandHandler("newcommand", new_command_function))
```

## 10. 部署建议

### 本地运行（开发）
```bash
python3 src/telegram_bot.py
```

### 服务器运行（生产）
```bash
# 使用nohup在后台运行
nohup python3 src/telegram_bot.py > bot.log 2>&1 &

# 使用systemd服务（推荐）
# 创建服务文件：/etc/systemd/system/telegram-bot.service
```

### Docker容器
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/telegram_bot.py"]
```

## 11. 联系支持

如有问题，请联系：
- 开发者：openhands-hotaru
- 邮箱：openhands@all-hands.dev
- 项目仓库：当前工作目录