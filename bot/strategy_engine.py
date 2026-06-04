from dataclasses import dataclass
from .market_data import fetch_candles


@dataclass
class SignalResult:
    symbol: str
    signal: str  # BUY / SELL / NONE
    confidence: float
    reason: str


# =========================
# REAL MARKET ANALYSIS
# =========================
def analyze_market(symbol: str):

    data = fetch_candles(symbol, 50)

    if not data or len(data["close"]) < 10:
        return None

    close = data["close"]

    # simple real trend
    latest = close[-1]
    prev = close[-5]

    trend_strength = abs(latest - prev)

    # RSI-like simple calculation (no fake random)
    gains = 0
    losses = 0

    for i in range(1, len(close)):
        diff = close[i] - close[i - 1]
        if diff > 0:
            gains += diff
        else:
            losses += abs(diff)

    rs = gains / (losses + 0.0001)
    rsi = 100 - (100 / (1 + rs))

    return {
        "rsi": rsi,
        "trend_strength": trend_strength,
        "price": latest
    }


# =========================
# SIGNAL GENERATOR
# =========================
def generate_signal_engine(symbol: str):

    data = analyze_market(symbol)

    if data is None:
        return None

    rsi = data["rsi"]
    trend = data["trend_strength"]
    price = data["price"]

    signal = "NONE"
    confidence = 0.40
    reason = []

    # BUY RULE
    if rsi < 35 and trend > 0:
        signal = "BUY"
        confidence = 0.70 + min(trend * 0.2, 0.2)
        reason.append("Oversold + bullish movement")

    # SELL RULE
    elif rsi > 65 and trend > 0:
        signal = "SELL"
        confidence = 0.70 + min(trend * 0.2, 0.2)
        reason.append("Overbought + bearish movement")

    else:
        reason.append("No strong confirmation")

    return SignalResult(
        symbol=symbol,
        signal=signal,
        confidence=round(confidence, 2),
        reason=" | ".join(reason)
    )