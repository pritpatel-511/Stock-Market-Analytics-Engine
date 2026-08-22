import numpy as np


def stock_returns(stock):
    close = np.array(stock["close"])

    if len(close) == 0:
        return None

    today = close[1:]
    yesterday = close[:-1]

    daily_returns = (today - yesterday) / yesterday
    total_return_days = len(daily_returns)
    average_return = np.mean(daily_returns)
    highest_return = np.max(daily_returns)
    lowest_return = np.min(daily_returns)
    positive_days = np.sum(daily_returns > 0)
    negative_days = np.sum(daily_returns < 0)
    zero_returns_days = np.sum(daily_returns == 0)
    return_volatility = np.std(daily_returns)

    # Cumulative Return
    first_close = close[0]
    last_close = close[-1]
    cumulative_return = (last_close - first_close) / first_close

    if total_return_days > 0:
        winning_percentage = positive_days / total_return_days * 100
    else:
        winning_percentage = 0

    return {
        "daily_returns": daily_returns,
        "total_return_days": total_return_days,
        "average_return": average_return,
        "highest_return": highest_return,
        "lowest_return": lowest_return,
        "positive_days": positive_days,
        "negative_days": negative_days,
        "zero_return_days": zero_returns_days,
        "return_volatility": return_volatility,
        "winning_percentage": winning_percentage,
        "cumulative_return": cumulative_return,
    }


def display_returns(stock_returns):
    print("\n" + "━" * 60)
    print(" 📈 DAILY RETURNS ANALYSIS")
    print("━" * 60)

    print(f"{'Daily Returns':30}: {len(stock_returns['daily_returns'])} Values")
    print(f"{'Average Returns':30}: {(stock_returns['average_return'])*100:.2f}%")
    print(f"{'Highest Return':30}: {(stock_returns['highest_return'])*100:.2f}%")
    print(f"{'Lowest Return':30}: {(stock_returns['lowest_return'])*100:.2f}%")
    print(f"{'Total Return Days':30}: {stock_returns['total_return_days']}")
    print(f"{'Positive Days':30}: {stock_returns['positive_days']}")
    print(f"{'Negative Days':30}: {stock_returns['negative_days']}")
    print(f"{'Zero Return Days':30}: {stock_returns['zero_return_days']}")
    print(f"{'Return Volatility':30}: {(stock_returns['return_volatility'])*100:.2f}%")
    print(f"{'Winning Percentage':30}: {stock_returns['winning_percentage']:.2f}%")
    print(f"{'Cumulative Return':30}: {(stock_returns['cumulative_return'])*100:.2f}%")
