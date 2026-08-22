import numpy as np


def moving_avg(close, window):
    weights = np.ones(window) / window

    sma_valid = np.convolve(close, weights, mode="valid")

    padding = np.full(window - 1, np.nan)

    return np.concatenate((padding, sma_valid))


def trend_analyze(stock):
    close = stock["close"]

    if len(close) == 0:
        return None

    SHORT_WINDOW = 5
    LONG_WINDOW = 20
    SMALL_THRESHOLD = 0.5

    moving_average_5 = moving_avg(close, SHORT_WINDOW)
    moving_average_20 = moving_avg(close, LONG_WINDOW)

    latest_ma5 = moving_average_5[-1]
    latest_ma20 = moving_average_20[-1]

    ma_difference_pct = ((latest_ma5 - latest_ma20) / latest_ma20) * 100

    if abs(ma_difference_pct) < SMALL_THRESHOLD:
        current_trend = "Sideways"
    elif ma_difference_pct > 0:
        current_trend = "Bullish"
    else:
        current_trend = "Bearish"

    highest_ma20 = np.nanmax(moving_average_20)
    lowest_ma20 = np.nanmin(moving_average_20)

    highest_ma5 = np.nanmax(moving_average_5)
    lowest_ma5 = np.nanmin(moving_average_5)

    with np.errstate(invalid="ignore"):
        bullish_days = np.sum(moving_average_5 > moving_average_20)
        bearish_days = np.sum(moving_average_5 < moving_average_20)

    total_days = bullish_days + bearish_days

    latest_close = close[-1]
    price_vs_ma20_pct = (latest_close - latest_ma20) / latest_ma20 * 100

    ma_bullish = latest_ma5 > latest_ma20
    price_bullish = latest_close > latest_ma20

    trend_score = 0
    if ma_bullish:
        trend_score += 1
    else:
        trend_score -= 1

    if price_bullish:
        trend_score += 1
    else:
        trend_score -= 1

    ma_difference = moving_average_5 - moving_average_20
    golden_cross = (ma_difference[:-1] <= 0) & (ma_difference[1:] > 0)
    death_cross = (ma_difference[:-1] >= 0) & (ma_difference[1:] < 0)

    golden_cross_count = np.sum(golden_cross)
    death_cross_count = np.sum(death_cross)

    if total_days != 0:
        bullish_ratio = bullish_days / total_days
    else:
        bullish_ratio = 0

    cross_balance = golden_cross_count - death_cross_count
    total_crosses = golden_cross_count + death_cross_count
    if total_crosses != 0:
        cross_score = (cross_balance / total_crosses + 1) / 2
    else:
        cross_score = 0.5

    trend_score_normalized = (trend_score + 2) / 4
    trend_strength_score = (
        trend_score_normalized * 0.4 + bullish_ratio * 0.3 + cross_score * 0.3
    ) * 100

    if trend_strength_score >= 75:
        trend_strength = "Strong Bullish"
    elif trend_strength_score >= 60:
        trend_strength = "Bullish"
    elif trend_strength_score >= 40:
        trend_strength = "Neutral"
    elif trend_strength_score >= 25:
        trend_strength = "Bearish"
    else:
        trend_strength = "Strong Bearish"

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
        "latest_close": latest_close,
        "price_vs_ma20_pct": price_vs_ma20_pct,
        "trend_score": trend_score,
        "golden_cross_count": golden_cross_count,
        "death_cross_count": death_cross_count,
        "cross_balance": cross_balance,
        "cross_score": cross_score,
        "bullish_ratio": bullish_ratio,
        "trend_strength_score": trend_strength_score,
        "trend_strength": trend_strength,
    }


def display_trend(trend_data):
    print("\n" + "━" * 60)
    print(" 🚀 TREND & MOVING AVERAGES")
    print("━" * 60)

    print(f"{'Latest 5-Days Moving Average':30}- {trend_data['latest_ma5']:.2f}")
    print(f"{'Latest 20-Days Moving Average':30}- {trend_data['latest_ma20']:.2f}")
    print(f"{'Current Trend':30}- {trend_data['current_trend']}")
    print(f"{'Highest 20-Days Moving Average':30}- {trend_data['highest_ma20']:.2f}")
    print(f"{'Lowest 20-Days Moving Average':30}- {trend_data['lowest_ma20']:.2f}")
    print(f"{'Highest 5-Days Moving Average':30}- {trend_data['highest_ma5']:.2f}")
    print(f"{'Lowest 5-Days Moving Average':30}- {trend_data['lowest_ma5']:.2f}")
    print(f"{'Total Bullish Days':30}- {trend_data['bullish_days']}")
    print(f"{'Total Bearish Days':30}- {trend_data['bearish_days']}")
    print(f"{'Latest Closing Price':30}- {trend_data['latest_close']:.2f}")
    print(f"{'Price vs 20-Day MA':30}- {trend_data['price_vs_ma20_pct']:.2f}%")
    print(f"{'Trend Score':30}- {trend_data['trend_score']}")
    print(f"{'Golden Cross Count':30}- {trend_data['golden_cross_count']}")
    print(f"{'Death Cross Count':30}- {trend_data['death_cross_count']}")
    print(f"{'Cross Balance':30}- {trend_data['cross_balance']:+d}")
    print(f"{'Cross Score':30}- {trend_data['cross_score']* 100:.2f}/100")
    print(f"{'Bullish Day Ratio':30}- {trend_data['bullish_ratio'] * 100:.2f}%")
    print(f"{'Trend Strength Score':30}- {trend_data['trend_strength_score']:.2f}/100")
    print(f"{'Trend Strength':30}- {trend_data['trend_strength']}")


def trend_strength_ranking(trend_result):
    ranking = sorted(
        trend_result.items(),
        key=lambda item: item[1]["trend_strength_score"],
        reverse=True,
    )
    print("\n" + "=" * 60)
    print(f"{'TREND STRENGTH RANKING':^60}")
    print("=" * 60)

    for rank, (company, data) in enumerate(ranking, start=1):
        print(
            f"{rank:02}. {company:20}"
            f"{data['trend_strength_score']:.2f}/100 "
            f"{data['trend_strength']}"
        )
