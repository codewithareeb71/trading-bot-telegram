from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from .market_data import last_close_price, get_trend
from .logger import logger


# =========================
# SIGNAL MODEL
# =========================
@dataclass
class TradeSignal:
    symbol: str
    signal_type: str   # BUY / SELL / NEUTRAL
    entry_time: str
    expiry_time: str
    confidence: float
    trend: str
    price: float


# =========================
# SIGNAL ENGINE (STABLE)
# =========================
def generate_signal(symbol: str) -> Optional[TradeSignal]:

    # 1. FETCH DATA
    price = last_close_price(symbol)
    trend_data = get_trend(symbol)

    # 2. SAFETY CHECK (IMPORTANT)
    if price is None or price <= 0:
        logger.warning("Market data unavailable for %s", symbol)
        return None

    # 3. SAFE TREND PARSING
    direction = "UNKNOWN"
    if isinstance(trend_data, dict):
        direction = trend_data.get("direction", "UNKNOWN")

    # 4. DEFAULT VALUES
    signal_type = "NEUTRAL"
    confidence = 0.50

    # 5. SIMPLE LOGIC ENGINE
    if direction == "bullish":
        signal_type = "BUY"
        confidence = 0.72

        # small boost if strong price
        if price > 1:
            confidence += 0.03

    elif direction == "bearish":
        signal_type = "SELL"
        confidence = 0.72

        if price > 1:
            confidence += 0.03

    else:
        signal_type = "NEUTRAL"
        confidence = 0.45

    # 6. CLAMP CONFIDENCE (SAFE RANGE)
    confidence = max(0.30, min(confidence, 0.90))

    # 7. TIME SETTINGS
    entry_time = datetime.utcnow().isoformat() + "Z"
    expiry_time = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z"

    # 8. RETURN SIGNAL
    return TradeSignal(
        symbol=symbol,
        signal_type=signal_type,
        entry_time=entry_time,
        expiry_time=expiry_time,
        confidence=round(confidence, 2),
        trend=direction,
        price=float(price)
    )