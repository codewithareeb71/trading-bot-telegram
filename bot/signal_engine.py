from dataclasses import dataclass
from datetime import datetime, timedelta

from .market_data import last_close_price, get_trend


@dataclass
class SignalResponse:
    status: str          # SIGNAL / WAIT
    symbol: str = ""
    direction: str = ""
    confidence: float = 0.0
    price: float = 0.0
    time: str = ""
    message: str = ""
    next_signal: str = ""


# =========================
# NEXT SIGNAL TIME
# =========================
def get_next_signal_time():
    return (datetime.utcnow() + timedelta(minutes=5)).strftime("%H:%M UTC")


# =========================
# MAIN ENGINE
# =========================
def generate_signal(symbol="EUR_USD"):

    price = last_close_price(symbol)
    trend = get_trend(symbol)

    # NO DATA
    if price is None:
        return SignalResponse(
            status="WAIT",
            message="Unable to fetch live market data.",
            next_signal=get_next_signal_time()
        )

    direction = trend.get("direction", "UNKNOWN")

    # BUY SIGNAL
    if direction == "bullish":
        return SignalResponse(
            status="SIGNAL",
            symbol=symbol,
            direction="BUY",
            confidence=82.0,
            price=round(float(price), 5),
            time=datetime.utcnow().strftime("%H:%M UTC"),
            message="Bullish momentum detected."
        )

    # SELL SIGNAL
    elif direction == "bearish":
        return SignalResponse(
            status="SIGNAL",
            symbol=symbol,
            direction="SELL",
            confidence=82.0,
            price=round(float(price), 5),
            time=datetime.utcnow().strftime("%H:%M UTC"),
            message="Bearish momentum detected."
        )

    # SIDEWAYS MARKET
    return SignalResponse(
        status="WAIT",
        message="Market is ranging. Waiting for breakout confirmation.",
        next_signal=get_next_signal_time()
    )