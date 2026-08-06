import numpy as np


def moving_avg(close, window):
    moving_arr = []
    for i in range(len(close) - window + 1):
        ma = np.mean(close[i : i + window])
        moving_arr.append(ma)
    return np.array(moving_arr)


def trend_analyze(stock):
    close = stock["close"]

    SHORT_WINDOW = 5
    LONG_WINDOW = 20
    SMALL_THRESHOLD = 0.01

    moving_average_5 = moving_avg(close, 5)
    moving_average_20 = moving_avg(close, 20)

    latest_ma5 = moving_average_5[-1]
    latest_ma20 = moving_average_20[-1]

    
    if latest_ma5 > latest_ma20:
        current_trend = "Bullish"
    elif abs(latest_ma5 - latest_ma20) < SMALL_THRESHOLD:
        current_trend = "Sideways"
    else:
        current_trend = "Bearish"

    highest_ma20 = np.max(moving_average_20)
    lowest_ma20 = np.min(moving_average_20)

    highest_ma5 = np.max(moving_average_5)
    lowest_ma5 = np.min(moving_average_5)

    offset = LONG_WINDOW - SHORT_WINDOW
    alligned_ma5 = moving_average_5[offset:]
    alligned_ma20 = moving_average_20
    bullish_days = np.sum(alligned_ma5 > alligned_ma20)
    bearish_days = np.sum(alligned_ma5 < alligned_ma20)

    latest_close = close[-1]
    trend_strength = (latest_close - latest_ma20) / latest_ma20 * 100

    return {
        "latest_ma5": latest_ma5,
        "latest_ma20": latest_ma20,
        "current_trend": current_trend,
        "highest_ma20": highest_ma20,
        "lowest_ma20": lowest_ma20,
        "highest_ma5": highest_ma5,
        "lowest_ma5": lowest_ma5,
        "bullish_days": bullish_days,
        "bearish_days": bearish_days,
        "trend_strength": trend_strength,
    }

def display_trend(company_name,trend_data):
    print("=" * 60)
    print(f"{company_name:^60}")
    print("=" * 60)

    print(f"{'Latest 5-Days Moving Average':30}- {trend_data['latest_ma5']:.2f}")
    print(f"{'Latest 20-Days Moving Average':30}- {trend_data['latest_ma20']:.2f}")
    print(f"{'Current Trend':30}- {trend_data['current_trend']}")
    print(f"{'Highest 20-Days Moving Average':30}- {trend_data['highest_ma20']:.2f}")
    print(f"{'Lowest 20-Days Moving Average':30}- {trend_data['lowest_ma20']:.2f}")
    print(f"{'Highest 5-Days Moving Average':30}- {trend_data['highest_ma5']:.2f}")
    print(f"{'Lowest 5-Days Moving Average':30}- {trend_data['lowest_ma5']:.2f}")
    print(f"{'Total Bullish Days':30}- {trend_data['bullish_days']}")
    print(f"{'Total Bearish Days':30}- {trend_data["bearish_days"]}")
    print(f"{'Trend Strength'}- {trend_data['trend_strength']}")