import numpy as np
from src import trend


def generate_ma_signals(stock, short_window=20, long_window=50):

    dates = stock["dates"]
    close = stock["close"]

    if len(close) < long_window:
        return None

    short_ma = trend.moving_avg(close, short_window)
    long_ma = trend.moving_avg(close, long_window)

    short_today = short_ma[1:]
    long_today = long_ma[1:]

    short_yesterday = short_ma[:-1]
    long_yesterday = long_ma[:-1]

    with np.errstate(invalid="ignore"):
        buy_mask = (short_today > long_today) & (short_yesterday <= long_yesterday)

        sell_mask = (short_today < long_today) & (short_yesterday >= long_yesterday)

        buy_indices = np.where(buy_mask)[0] + 1
        sell_indices = np.where(sell_mask)[0] + 1

    buy_signals = [{"date": dates[i], "price": close[i]} for i in buy_indices]
    sell_signals = [{"date": dates[i], "price": close[i]} for i in sell_indices]

    return {
        "short_window": short_window,
        "long_window": long_window,
        "buy_signals": buy_signals,
        "sell_signals": sell_signals,
        "total_buys": len(buy_signals),
        "total_sells": len(sell_signals),
    }


def display_signals(signal_data):
    if signal_data is None:
        print(f"Not enough data to calculate signals")
        return

    print("\n" + "━" * 60)
    print(" 📅 QUARTERLY BREAKDOWN")
    print("━" * 60)

    print(f"{'Total BUY Signals':30}- {signal_data['total_buys']}")
    print(f"{'Total SELL Signals':30}- {signal_data['total_sells']}")
    print("-" * 60)

    print("--- BUY SIGNALS (Golden Cross) ---")
    if signal_data["buy_signals"]:
        for signal in signal_data["buy_signals"]:
            print(f"Date: {signal['date']} | Price: {signal['price']:.2f}")
    else:
        print("No Buy Signals generated.")

    print("\n--- SELL SIGNALS (Death Cross) ---")
    if signal_data["sell_signals"]:
        for signal in signal_data["sell_signals"]:
            print(f"Date: {signal['date']} | Price: {signal['price']:.2f}")
    else:
        print("No Sell Signals generated.")