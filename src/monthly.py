import numpy as np
from datetime import datetime

def calculate_monthly_analytics(stock):
    dates = stock["dates"]
    close = stock["close"]
    high = stock["high"]
    low = stock["low"]
    volume = stock["volume"]

    if len(dates) == 0:
        return None

    dates = dates.astype("datetime64[D]")
    months = dates.astype("datetime64[M]")
    unique_months = np.unique(months)

    monthly_data = {}

    for month in unique_months:
        mask = months == month
        monthly_close = close[mask]
        monthly_high = high[mask]
        monthly_low = low[mask]
        monthly_volume= volume[mask]

        average_price = np.mean(monthly_close)
        monthly_highest = np.max(monthly_high)
        monthly_lowest = np.min(monthly_low)
        monthly_total_volume = np.sum(monthly_volume)

        monthly_first_close = monthly_close[0]
        monthly_last_close = monthly_close[-1]

        if monthly_first_close != 0:
            monthly_return = (
                (monthly_last_close - monthly_first_close) / monthly_first_close
            ) * 100
        else:
            monthly_return = 0

        month_label = datetime.strptime(str(month),"%Y-%m").strftime("%B-%Y")

        monthly_data[month_label] = {
            "average_price":average_price,
            "highest_price":monthly_highest,
            "lowest_price":monthly_lowest,
            "monthly_return":monthly_return,
            "total_volume" : monthly_total_volume
        }
    
    best_month = max(
        monthly_data,
        key=lambda month : monthly_data[month]["monthly_return"]
    )

    worst_month = min(
        monthly_data,
        key= lambda month: monthly_data[month]["monthly_return"]
    )

    return {
        "monthly_data":monthly_data,
        "best_month":best_month,
        "worst_month":worst_month
    }

def display_monthly(monthly_data):
    print("\n" + "━" * 60)
    print(" 📅 MONTHLY BREAKDOWN")
    print("━" * 60)

    for month,data in monthly_data['monthly_data'].items():

        print(f"\n{month}\n")
        print(f"{'Average Price':30}- {data['average_price']:.2f}")
        print(f"{'Highest Price':30}- {data['highest_price']:.2f}")
        print(f"{'Lowest Price':30}- {data['lowest_price']:.2f}")
        print(f"{'Monthly Return':30}- {data['monthly_return']:.2f}%")
        print(f"{'Total Volume':30}- {data['total_volume']}")

        print("-"*60)

    print(f"{'Best Month':30}- {monthly_data['best_month']}")
    print(f"{'Worst Month':30}- {monthly_data['worst_month']}")