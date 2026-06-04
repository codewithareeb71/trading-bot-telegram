import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set. Please configure it in Railway.")

# OANDA
OANDA_API_KEY = os.getenv("OANDA_API_KEY")
OANDA_BASE_URL = "https://api-fxpractice.oanda.com"

# Default settings
DEFAULT_SYMBOL = "EUR_USD"
GRANULARITY = "M1"