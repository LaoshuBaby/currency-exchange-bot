#!/usr/bin/env python3
"""
实际可运行的Telegram机器人
需要从 @BotFather 获取API Token
"""

import os
import logging
import json
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# 导入汇率查询模块
try:
    from currency import get_rate, get_rate_with_info, get_supported_currencies, get_supported_providers
except ImportError:
    # 如果直接导入失败，尝试相对导入
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.currency import get_rate, get_rate_with_info, get_supported_currencies, get_supported_providers

# 设置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 从环境变量获取Bot Token（推荐方式）
# 或者在代码中直接设置（不推荐用于生产环境）
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    user = update.effective_user
    welcome_text = f"""
🎉 Hello World! 欢迎 {user.first_name}！

🤖 我是汇率查询机器人，可以帮你：
• 查询各种货币汇率
• 显示当前东京时间
• 进行货币换算

📋 可用命令：
/start - 显示此欢迎信息
/help - 查看详细帮助
/exchange [金额] [货币] [货币] - 货币兑换查询
/time - 显示当前东京时间
/about - 关于此机器人

💡 示例：
/exchange 100 JPY CNY - 查询100日元兑人民币
/exchange 1 USD EUR - 查询1美元兑欧元
/exchange JPY CNY - 查询1日元兑人民币
/time - 显示当前东京时间

🚀 开始使用吧！
"""
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令"""
    help_text = """
📚 帮助文档

🤖 机器人功能：
1. 货币兑换查询 - 支持多种货币兑换
2. 时间查询 - 显示东京时间
3. 汇率换算 - 快速计算金额

📋 命令列表：
/start - 开始使用机器人
/help - 显示此帮助信息
/exchange [金额] [来源货币] [目标货币] - 货币兑换查询
    格式1：/exchange 100 JPY CNY (查询100日元兑人民币)
    格式2：/exchange JPY CNY (查询1日元兑人民币)
    示例：/exchange 1 USD EUR
    示例：/exchange 5000 KRW JPY
/time - 显示当前东京时间
/about - 关于此机器人
	/list - 列出所有支持的货币代码

💰 支持的货币代码：

💵 主要法币：
USD - 美元        EUR - 欧元
GBP - 英镑        JPY - 日元
CNY - 人民币      HKD - 港币
KRW - 韩元        AUD - 澳元
CAD - 加元        SGD - 新加坡元

🔗 加密货币（仅Google Finance支持）：
BTC - 比特币      ETH - 以太坊
BNB - 币安币      XRP - 瑞波币
ADA - 卡尔达诺    SOL - Solana
DOGE - 狗狗币

🔧 技术信息：
• 使用 python-telegram-bot 库
• 时区：东京时间 (Asia/Tokyo)
• 开发者：openhands-hotaru
• 汇率数据：Frankfurter API (实时汇率)
"""
    await update.message.reply_text(help_text)

async def exchange_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /exchange 命令 - 货币兑换查询"""
    # 解析参数：支持两种格式：
    # 1. /exchange 100 JPY CNY (金额 来源货币 目标货币)
    # 2. /exchange JPY CNY (默认金额为1)
    
    if not context.args:
        await update.message.reply_text(
            "❌ 使用方法：/exchange [金额] [来源货币] [目标货币]\n\n"
            "💡 示例：\n"
            "/exchange 100 JPY CNY - 查询100日元兑人民币\n"
            "/exchange 1 USD EUR - 查询1美元兑欧元\n"
            "/exchange 5000 KRW JPY - 查询5000韩元兑日元\n"
            "/exchange JPY CNY - 查询1日元兑人民币\n\n"
            "📋 常用货币代码：\n"
            "USD(美元), EUR(欧元), GBP(英镑)\n"
            "JPY(日元), CNY(人民币), HKD(港币)\n"
            "KRW(韩元), AUD(澳元), CAD(加元)"
        )
        return
    
    # 解析参数
    args = context.args
    amount = 1.0  # 默认金额
    from_currency = ""
    to_currency = ""
    
    if len(args) == 2:
        # 格式：/exchange JPY CNY
        from_currency = args[0].upper()
        to_currency = args[1].upper()
    elif len(args) == 3:
        # 格式：/exchange 100 JPY CNY
        try:
            amount = float(args[0])
            if amount <= 0:
                await update.message.reply_text("❌ 金额必须大于0")
                return
        except ValueError:
            await update.message.reply_text("❌ 金额必须是数字")
            return
        from_currency = args[1].upper()
        to_currency = args[2].upper()
    else:
        await update.message.reply_text(
            "❌ 参数格式不正确\n\n"
            "正确格式：\n"
            "/exchange [金额] [来源货币] [目标货币]\n"
            "或 /exchange [来源货币] [目标货币]\n\n"
            "示例：\n"
            "/exchange 100 JPY CNY\n"
            "/exchange JPY CNY"
        )
        return
    
    # 获取汇率（使用真实API）
    try:
        # 使用get_rate_with_info获取包含提供者信息的完整结果
        rate_info = get_rate_with_info(from_currency, to_currency, amount)
        
        if rate_info.get('success') and rate_info.get('result') is not None:
            result = rate_info['result']
            provider_name = rate_info['provider']
            
            # 计算汇率（每单位）
            rate = result / amount if amount > 0 else 0
            
            response = f"💱 货币兑换查询\n\n"
            response += f"📊 查询详情：\n"
            response += f"• 金额：{amount:,.2f} {from_currency}\n"
            response += f"• 目标：{to_currency}\n"
            response += f"• 汇率：1 {from_currency} = {rate:.6f} {to_currency}\n\n"
            
            response += f"💰 兑换结果：\n"
            response += f"**{amount:,.2f} {from_currency} ≈ {result:,.2f} {to_currency}**\n\n"
            
            # 显示常见金额换算（基于一次查询结果计算，不重复查询）
            if amount != 1:
                response += f"📈 其他金额换算：\n"
                common_amounts = [1, 10, 50, 100, 500, 1000]
                for common_amount in common_amounts:
                    if common_amount != amount:
                        common_converted = common_amount * rate
                        response += f"{common_amount:5,d} {from_currency} ≈ {common_converted:10.2f} {to_currency}\n"
            
            # 显示反向汇率
            if rate > 0:
                reverse_rate = 1 / rate
                response += f"\n🔄 反向汇率：\n"
                response += f"1 {to_currency} = {reverse_rate:.4f} {from_currency}"
            
            response += f"\n\n⏰ 查询时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            response += f"\n📍 时区：东京时间 (JST)"
            response += f"\n📊 数据来源：{provider_name}"
            
        else:
            error_msg = rate_info.get('error', '未知错误')
            response = f"❌ 无法获取 {from_currency} 到 {to_currency} 的汇率\n\n"
            response += f"错误信息：{error_msg}\n\n"
            response += "可能原因：\n"
            response += "• 货币代码不正确\n"
            response += "• 该货币对暂不支持\n"
            response += "• 汇率数据暂时不可用\n\n"
            response += "💡 请使用 /help 查看支持的货币代码"
            
    except Exception as e:
        logger.error(f"汇率查询失败: {e}")
        response = f"❌ 汇率查询失败\n\n"
        response += f"错误信息：{str(e)}\n\n"
        response += "请稍后重试或联系管理员"
    
    await update.message.reply_text(response)

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /time 命令"""
    # 获取当前东京时间
    current_time = datetime.now()
    
    time_text = f"""
⏰ 当前时间信息：

🌍 东京时间 (JST):
{current_time.strftime('%Y年%m月%d日 %H:%M:%S')}

📅 日期格式：
{current_time.strftime('%A, %B %d, %Y')}
{current_time.strftime('第%W周，第%j天')}

🕐 24小时制：{current_time.strftime('%H:%M:%S')}
🕙 12小时制：{current_time.strftime('%I:%M:%S %p')}

📍 系统时区：Asia/Tokyo
⚙️ 机器人状态：运行中
"""
    await update.message.reply_text(time_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /about 命令"""
    about_text = """
🤖 关于汇率查询机器人

📱 版本：1.0.0
📅 创建日期：2026年3月2日
📍 时区：东京时间 (Asia/Tokyo)

👨‍💻 开发者：openhands-hotaru
📧 邮箱：openhands@all-hands.dev

🔧 技术栈：
• Python 3.12+
• python-telegram-bot 库
• 多汇率API支持
• 东京时间同步

📚 功能特点：
1. 多货币汇率查询
2. 实时时间显示
3. 货币金额换算
4. 用户友好的交互界面

⚠️ 免责声明：
本机器人提供的汇率数据仅供参考，
实际汇率以银行柜台成交价为准。

🚀 未来计划：
• 集成真实汇率API
• 添加历史汇率查询
• 支持更多货币
• 添加图表显示

❤️ 感谢使用！
"""
    await update.message.reply_text(about_text)

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /list 命令 - 列出所有支持的货币代码"""
    try:
        # 获取支持的货币代码
        currencies = get_supported_currencies()
        
        # 分类显示
        fiat_currencies = []
        crypto_currencies = []
        other_currencies = []
        
        for code, name in currencies.items():
            if code in ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'USDT']:
                crypto_currencies.append((code, name))
            elif code in ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'HKD', 'KRW', 'AUD', 'CAD', 'SGD']:
                fiat_currencies.append((code, name))
            else:
                other_currencies.append((code, name))
        
        # 构建响应
        response = "📋 **所有支持的货币代码列表**\n\n"
        
        response += "💵 **主要法币**\n"
        for code, name in sorted(fiat_currencies):
            response += f"• {code} - {name}\n"
        
        response += "\n🌏 **其他法币**\n"
        for code, name in sorted(other_currencies):
            response += f"• {code} - {name}\n"
        
        response += "\n🔗 **加密货币**\n"
        response += "（仅Google Finance支持）\n"
        for code, name in sorted(crypto_currencies):
            response += f"• {code} - {name}\n"
        
        response += f"\n📊 **总计：{len(currencies)} 种货币**\n"
        response += f"💵 法币：{len(fiat_currencies) + len(other_currencies)} 种\n"
        response += f"🔗 加密货币：{len(crypto_currencies)} 种\n\n"
        
        response += "💡 **使用提示：**\n"
        response += "1. 本列表仅显示系统已知的货币代码\n"
        response += "2. 您可以尝试查询任何3-4位字母的货币代码\n"
        response += "3. 实际支持情况取决于API提供商\n"
        response += "4. 加密货币查询请使用：/exchange BTC USD --provider google_finance\n\n"
        
        response += "🔧 **支持的API提供商：**\n"
        providers = get_supported_providers()
        for provider in providers:
            response += f"• {provider}\n"
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"列出货币代码失败: {e}")
        await update.message.reply_text(
            "❌ 列出货币代码失败\n\n"
            f"错误信息：{str(e)}\n\n"
            "请稍后重试或联系管理员"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理普通文本消息"""
    user_message = update.message.text
    
    # 如果消息看起来像货币查询（但不是命令）
    if len(user_message.split()) == 2 and len(user_message) <= 10:
        parts = user_message.upper().split()
        if len(parts[0]) == 3 and len(parts[1]) == 3:
            # 可能是货币代码，提供帮助
            await update.message.reply_text(
                f"检测到可能的货币代码：{parts[0]} {parts[1]}\n\n"
                f"💡 想查询汇率吗？请使用：\n"
                f"/exchange {parts[0]} {parts[1]}\n\n"
                f"示例：/exchange 100 {parts[0]} {parts[1]}"
            )
            return
    
    # 默认回复
    await update.message.reply_text(
        f"👋 你好！你发送了：{user_message}\n\n"
        f"我是汇率查询机器人，可以帮你：\n"
        f"• 查询货币汇率 - 使用 /exchange 100 JPY CNY\n"
        f"• 查看当前时间 - 使用 /time\n"
        f"• 获取帮助信息 - 使用 /help\n\n"
        f"试试这些命令吧！"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理错误"""
    logger.error(f"更新 {update} 导致错误 {context.error}")
    
    try:
        await update.message.reply_text(
            "❌ 抱歉，处理您的请求时出错了！\n\n"
            "可能的原因：\n"
            "• 网络连接问题\n"
            "• 命令格式不正确\n"
            "• 机器人暂时不可用\n\n"
            "💡 请稍后重试或使用 /help 查看正确用法。"
        )
    except:
        pass  # 如果无法发送消息，静默失败

def main():
    """启动机器人主函数"""
    print("=" * 60)
    print("🤖 Telegram汇率查询机器人")
    print("=" * 60)
    
    # 检查Bot Token
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n❌ 错误：未设置有效的Bot Token！")
        print("\n📋 设置步骤：")
        print("1. 在Telegram中搜索 @BotFather")
        print("2. 发送 /newbot 创建新机器人")
        print("3. 按照提示设置机器人名称和用户名")
        print("4. 获取API Token（类似：1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ）")
        print("\n🔧 配置方法（任选其一）：")
        print("A. 直接修改代码：将BOT_TOKEN替换为你的token")
        print("B. 设置环境变量：export TELEGRAM_BOT_TOKEN='你的token'")
        print("C. 创建.env文件：TELEGRAM_BOT_TOKEN=你的token")
        print("\n🚀 配置完成后重新运行此脚本")
        return
    
    print(f"\n✅ Bot Token已设置")
    print(f"⏰ 系统时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📍 系统时区：Asia/Tokyo (JST)")
    print(f"👤 Git用户：openhands-hotaru")
    
    try:
        # 创建Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # 添加命令处理器
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("exchange", exchange_command))
        application.add_handler(CommandHandler("time", time_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("list", list_command))
        
        # 添加消息处理器（处理非命令消息）
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # 添加错误处理器
        application.add_error_handler(error_handler)
        
        print("\n🚀 机器人启动成功！")
        print("📱 在Telegram中搜索你的机器人用户名开始使用")
        print("⏳ 按 Ctrl+C 停止机器人")
        print("=" * 60)
        
        # 启动轮询
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        
    except Exception as e:
        print(f"\n❌ 启动机器人失败：{e}")
        print("\n🔧 可能的原因：")
        print("1. Bot Token无效或已过期")
        print("2. 网络连接问题")
        print("3. python-telegram-bot库版本问题")
        print("\n💡 解决方案：")
        print("1. 检查Bot Token是否正确")
        print("2. 确保网络连接正常")
        print("3. 尝试重新安装依赖：pip install python-telegram-bot")

if __name__ == '__main__':
    main()