import numpy as np

def company_statistics(stock):
    close = stock["close"]
    trade_days = len(close)
    mean = np.mean(close)
    median = np.median(close)
    high_close = np.max(close)
    low_close = np.min(close)
    price_range = high_close - low_close
    average_daily_range = np.mean(stock["high"] - stock["low"])
    variance = np.var(close)
    #standard deviation
    std_dev = np.std(close)
    #co-efficient of variation
    if mean!=0:
        cv = std_dev / mean
    else:
        cv = 0
    percentile = np.percentile(close,[25,50,75])

    return {
        "trading_days":trade_days,
        "average_price":mean,
        "median_price":median,
        "highest_close":high_close,
        "lowest_close":low_close,
        "price_range":price_range,
        "average_daily_range":average_daily_range,
        "variance":variance,
        "standard_deviation":std_dev,
        "coefficient_of_variation":cv,
        "percentiles": {
            "25":percentile[0],
            "50":percentile[1],
            "75":percentile[2],
        }
    }

def display_statistics(company_name,stats):
    print("=" * 60)
    print(f"{company_name:^60}")
    print("=" * 60)

    print(f"{'Trading Days':30} : {stats['trading_days']}")
    print(f"{'Average Price':30} : {stats['average_price']:.2f}")
    print(f"{'Median Price':30} : {stats['median_price']:.2f}")
    print(f"{'Highest Closing':30} : {stats['highest_close']:.2f}")
    print(f"{'Lowest Closing':30} : {stats['lowest_close']:.2f}")
    print(f"{'Price Range':30} : {stats['price_range']:.2f}")
    print(f"{'Average Daily Range':30} : {stats['average_daily_range']:.2f}")
    print(f"{'Variance':30} : {stats['variance']:.2f}")
    print(f"{'Standard Deviation':30} : {stats['standard_deviation']:.2f}")
    print(f"{'Coefficient of Variation':30} : {stats['coefficient_of_variation']:.4f}")

    print("-" * 60)
    print(f"{'Percentiles':^60}")
    print("-" * 60)

    print(f"{'25th Percentile':30} : {stats['percentiles']['25']:.2f}")
    print(f"{'50th Percentile (Median)':30} : {stats['percentiles']['50']:.2f}")
    print(f"{'75th Percentile':30} : {stats['percentiles']['75']:.2f}")

    print("=" * 60)
    print()
