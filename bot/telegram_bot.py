from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from .signal_engine import generate_signal
from .config import TELEGRAM_BOT_TOKEN


# =========================
# BOT INIT
# =========================
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()


# =========================
# /signal COMMAND
# =========================
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    symbol = "EUR_USD"

    if context.args:
        symbol = context.args[0].upper()

    sig = generate_signal(symbol)

    # ❌ safety check
    if not sig:
        await update.message.reply_text("❌ Error analyzing market")
        return

    # ================= WAIT STATE =================
    if sig.status == "WAIT":
        msg = f"""
📊 MARKET STATUS

⚠️ {sig.message}

⏱ Next Signal Window: {sig.next_signal}

📡 Bot analyzing market continuously...
"""
        await update.message.reply_text(msg)
        return

    # ================= SIGNAL STATE =================
    msg = f"""
📊 SIGNAL CARD

Asset: {sig.symbol}
Direction: {sig.direction}
Price: {sig.price}

🔥 Confidence: {sig.confidence}%

⏱ Time: {sig.time}

📡 Status: ACTIVE TRADE SETUP
"""

    await update.message.reply_text(msg)


# =========================
# BOT RUN
# =========================
def run_bot():
    print("🚀 Bot running...")
    app.add_handler(CommandHandler("signal", signal))
    app.run_polling()