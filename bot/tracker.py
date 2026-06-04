from datetime import datetime

trades = []


def can_trade():
    now = datetime.utcnow()

    # keep only last 24h
    global trades
    trades = [t for t in trades if (now - t).seconds < 86400]

    return len(trades) < 3


def add_trade():
    trades.append(datetime.utcnow())


def stats():
    return {
        "wins": 0,
        "losses": 0,
        "winrate": 0
    }