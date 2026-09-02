import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from analysis import analyze_chart, format_analysis


TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
🤖 AI TRADING ANALYSIS BOT

স্বাগতম!

📷 আপনার Trading Chart-এর Screenshot পাঠান।

আমি analysis করে দেখানোর জন্য প্রস্তুত:

📈 Trend
🟢 Support
🔴 Resistance
📐 PPR
🕯️ Candle
📍 Entry Zone
✅ Confirmation
🎯 Signal

⚠️ এটি probability-based analysis।
100% profit guarantee নয়।
"""
    await update.message.reply_text(message)


async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 অনুগ্রহ করে আপনার Trading Chart-এর Screenshot পাঠান।"
    )


async def photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 Chart পেয়েছি!\n\n"
        "🔍 এখন chart analysis engine প্রস্তুত করা হচ্ছে..."
    )

    result = analyze_chart()
    analysis = format_analysis(result)

    await update.message.reply_text(analysis)


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is not configured.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo_message))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_message)
    )

    print("🤖 AI Trading Analysis Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
