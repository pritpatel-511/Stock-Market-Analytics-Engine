import numpy as np


def calculate_quarterly_analytics(stock):
    dates = stock["dates"]
    dates = dates.astype("datetime64[D]")
    
    month_number = (
        dates.astype("datetime64[M]") - dates.astype("datetime64[Y]")
    ).astype(int) + 1

    quarter_number = (month_number - 1) // 3 + 1
    years = dates.astype("datetime64[Y]")
    quarter_labels = np.array([f"Q{q}-{str(y)}" for q, y in zip(quarter_number, years)])

    unique_quarters = np.unique(quarter_labels)

    close = stock["close"]
    volume = stock["volume"]

    if len(close) == 0 or len(volume) == 0:
        return None

    quarterly_data = {}

    for quarter in unique_quarters:
        mask = quarter_labels == quarter

        quarter_close = close[mask]

        quarter_first_close = quarter_close[0]
        quarter_last_close = quarter_close[-1]

        if quarter_first_close != 0:
            quarter_return = (
                (quarter_last_close - quarter_first_close) / quarter_first_close
            ) * 100
        else:
            quarter_return = 0

        quarter_volume = volume[mask]

        average_volume = np.mean(quarter_volume)
        total_volume = np.sum(quarter_volume)

        average_price = np.mean(quarter_close)
        highest_price = np.max(quarter_close)
        lowest_price = np.min(quarter_close)

        quarterly_data[quarter] = {
            "quarter_return": quarter_return,
            "average_volume": average_volume,
            "total_volume": total_volume,
            "average_price": average_price,
            "highest_price": highest_price,
            "lowest_price": lowest_price,
        }

    best_quarter = max(
        quarterly_data, key=lambda quarter: quarterly_data[quarter]["quarter_return"]
    )
    worst_quarter = min(
        quarterly_data, key=lambda quarter: quarterly_data[quarter]["quarter_return"]
    )

    return {
        "quarterly_data": quarterly_data,
        "best_quarter": best_quarter,
        "worst_quarter": worst_quarter,
    }


def display_quarterly_analytics(company_name, quarterly_data):
    print("=" * 60)
    print(f"{company_name:^60}")
    print("=" * 60)

    for quarter, data in quarterly_data["quarterly_data"].items():
        print(f"\n{quarter}\n")
        print(f"{'Quarter Return':30}- {data['quarter_return']:.2f}%")
        print(f"{'Average Volume':30}- {data['average_volume']:.0f}")
        print(f"{'Total Volume':30}- {data['total_volume']:.0f}")
        print(f"{'Average Price':30}- {data['average_price']:.2f}")
        print(f"{'Highest Price':30}- {data['highest_price']:.2f}")
        print(f"{'Lowest Price':30}- {data['lowest_price']:.2f}")
    print("-" * 80)
    print(f"{'Best Quarter':30}- {quarterly_data['best_quarter']}")
    print(f"{'Worst Quarter':30}- {quarterly_data['worst_quarter']}")
