import numpy as np


def calculate_action(stock):
    high = stock["high"]

    if len(high) == 0:
        return None

    highest_high = np.max(high)

    low = stock["low"]

    if len(low) == 0:
        return None

    lowest_low = np.min(low)

    average_high = np.mean(high)
    average_low = np.mean(low)

    daily_range = high - low
    average_daily_range = np.mean(daily_range)

    biggest_intraday_move = np.max(daily_range)
    biggest_intraday_move_day = np.argmax(daily_range)
    biggest_intraday_move_date = stock["dates"][biggest_intraday_move_day]


    open_price = stock["open"]
    close = stock["close"]

    if len(open_price) == 0 or len(close) == 0:
        return None

    today_open = open_price[1:]
    yesterday_close = close[:-1]

    gap_up_mask = today_open > yesterday_close
    gap_up_days = np.sum(gap_up_mask)

    gap_down_mask = today_open < yesterday_close
    gap_down_days = np.sum(gap_down_mask)

    total_comparison_days = gap_up_days + gap_down_days

    if total_comparison_days == 0:
        gap_up_days_percentage = 0
    else:
        gap_up_days_percentage = gap_up_days / total_comparison_days * 100

    intraday_range_pct = ((high - low) / open_price) * 100
    average_intraday_range_pct = np.mean(intraday_range_pct)

    return {
        "highest_high": highest_high,
        "lowest_low": lowest_low,
        "average_high": average_high,
        "average_low": average_low,
        "average_daily_range": average_daily_range,
        "biggest_intraday_move": biggest_intraday_move,
        "biggest_intraday_move_date": biggest_intraday_move_date,
        "average_intraday_range_pct": average_intraday_range_pct,
        "gap_up_days": gap_up_days,
        "gap_down_days": gap_down_days,
        "gap_up_days_percentage": gap_up_days_percentage,
    }


def display_price_action(company_name, price_action_data):
    print("=" * 60)
    print(f"{company_name:^60}")
    print("=" * 60)

    print(f"{'Highest High':30}- {price_action_data['highest_high']:.2f}")
    print(f"{'Lowest Low':30}- {price_action_data['lowest_low']:.2f}")
    print(f"{'Average High':30}- {price_action_data['average_high']:.2f}")
    print(f"{'Average Low':30}- {price_action_data['average_low']:.2f}")
    print(f"{'Average Daily Range':30}- {price_action_data['average_daily_range']:.2f}")
    print(
        f"{'Biggest Intraday Move':30}- {price_action_data['biggest_intraday_move']:.2f}"
    )
    print(
        f"{'Biggest Intraday Move Date':30}- {price_action_data['biggest_intraday_move_date']}"
    )
    print(f"{'Average Intraday Range Percentage':30}- {price_action_data['average_intraday_range_pct']:.2f}%")
    print(f"{'Gap Up Days':30}- {price_action_data['gap_up_days']}")
    print(f"{'Gap Down Days':30}- {price_action_data['gap_down_days']}")
    print(
        f"{'Gap Up Days Percentage':30}- {price_action_data['gap_up_days_percentage']:.2f}%"
    )
