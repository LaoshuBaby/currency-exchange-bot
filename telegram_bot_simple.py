#!/usr/bin/env python3
"""
简单的Telegram机器人示例
发送 /start 命令会回复 "Hello World!"
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 设置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 你的Telegram Bot Token（从 @BotFather 获取）
# 注意：在实际使用中，不要将token硬编码在代码中，应该使用环境变量
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # 替换为你的实际token

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    user = update.effective_user
    await update.message.reply_text(
        f"Hello World! 👋\n"
        f"欢迎使用汇率查询机器人，{user.first_name}！\n\n"
        f"可用命令：\n"
        f"/start - 显示此消息\n"
        f"/help - 显示帮助信息\n"
        f"/rate [货币] - 查询汇率（示例：/rate JPY CNY）\n"
        f"/time - 显示当前东京时间"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令"""
    help_text = """
🤖 汇率查询机器人帮助

可用命令：
/start - 开始使用机器人
/help - 显示此帮助信息
/rate [来源货币] [目标货币] - 查询汇率
    示例：/rate JPY CNY (查询日元兑人民币汇率)
    示例：/rate USD CNY (查询美元兑人民币汇率)
/time - 显示当前东京时间

支持的货币代码：
USD - 美元, EUR - 欧元, GBP - 英镑
JPY - 日元, CNY - 人民币, HKD - 港币
KRW - 韩元, AUD - 澳元, CAD - 加元

更多功能开发中...
"""
    await update.message.reply_text(help_text)

async def rate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /rate 命令 - 查询汇率"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "使用方法：/rate [来源货币] [目标货币]\n"
            "示例：/rate JPY CNY\n"
            "示例：/rate USD CNY"
        )
        return
    
    from_currency = context.args[0].upper()
    to_currency = context.args[1].upper()
    
    # 这里可以调用我们之前写的汇率查询函数
    # 为了简化示例，我们先返回一个模拟响应
    await update.message.reply_text(
        f"查询汇率：{from_currency} → {to_currency}\n\n"
        f"模拟汇率数据（实际需要调用API）：\n"
        f"1 {from_currency} ≈ 0.05 {to_currency}\n"
        f"100 {from_currency} ≈ 5.00 {to_currency}\n\n"
        f"⚠️ 注意：这是模拟数据，实际汇率查询功能需要集成汇率API。"
    )

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /time 命令 - 显示当前时间"""
    from datetime import datetime
    import pytz
    
    # 获取东京时间
    tokyo_tz = pytz.timezone('Asia/Tokyo')
    tokyo_time = datetime.now(tokyo_tz)
    
    await update.message.reply_text(
        f"⏰ 当前东京时间：\n"
        f"{tokyo_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"时区：Asia/Tokyo (JST)"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """回显用户消息（非命令）"""
    await update.message.reply_text(
        f"你说：{update.message.text}\n\n"
        f"试试这些命令：\n"
        f"/start - 开始使用\n"
        f"/help - 查看帮助\n"
        f"/rate JPY CNY - 查询汇率"
    )

def main():
    """启动机器人"""
    # 创建Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加命令处理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rate", rate_command))
    application.add_handler(CommandHandler("time", time_command))
    
    # 添加消息处理器（处理非命令消息）
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # 启动机器人
    print("🤖 机器人正在启动...")
    print("⚠️  注意：需要将 BOT_TOKEN 替换为你的实际Telegram Bot Token")
    print("     从 @BotFather 获取token：https://t.me/BotFather")
    print("     然后运行：python3 telegram_bot_real.py")
    
    # 在实际运行前检查token
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n❌ 错误：请先设置正确的BOT_TOKEN！")
        print("1. 在Telegram中搜索 @BotFather")
        print("2. 发送 /newbot 创建新机器人")
        print("3. 获取API Token")
        print("4. 将token填入 telegram_bot_real.py 文件中")
        return
    
    # 开始轮询
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()