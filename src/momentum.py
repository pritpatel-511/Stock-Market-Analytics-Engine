import numpy as np


def calculate_monthly_return(stock):
    dates = stock["dates"]
    close = stock["close"]

    dates = dates.astype("datetime64[D]")
    months = dates.astype("datetime64[M]")
    unique_monthes = np.unique(months)

    monthly_returns = {}

    for month in unique_monthes:

        mask = months == month

        monthly_close = close[mask]

        first_close = monthly_close[0]
        last_close = monthly_close[-1]

        if first_close != 0:
            month_return = ((last_close - first_close) / first_close) * 100
        else:
            month_return = 0

        monthly_returns[str(month)] = month_return
    return monthly_returns


def calculate_quarterly_return(stock):
    dates = stock["dates"]
    close = stock["close"]

    dates = dates.astype("datetime64[D]")
    months = dates.astype("datetime64[M]")
    unique_monthes = np.unique(months)

    quarterly_returns = {}

    for i in range(0, len(unique_monthes), 3):
        quarter_months = unique_monthes[i : i + 3]

        mask = np.isin(months, quarter_months)

        quarterly_close = close[mask]

        quarter_start = quarterly_close[0]
        quarter_end = quarterly_close[-1]

        if quarter_start != 0:
            quarter_return = ((quarter_end - quarter_start) / quarter_start) * 100
        else:
            quarter_return = 0
        quarter_number = i // 3 + 1
        quarterly_returns[f"Q{quarter_number}"] = quarter_return
    return quarterly_returns


def calculate_momentum(stock):
    close = stock["close"]

    if len(close) == 0:
        return None

    first_price = close[0]
    last_price = close[-1]

    price_change = last_price - first_price
    if first_price != 0:
        annual_return = price_change / first_price * 100
    else:
        annual_return = 0

    monthly_returns = calculate_monthly_return(stock)

    quarterly_returns = calculate_quarterly_return(stock)

    return {
        "first_price": first_price,
        "last_price": last_price,
        "price_change": price_change,
        "annual_return": annual_return,
        "monthly_returns": monthly_returns,
        "quarterly_returns": quarterly_returns,
    }


def display_momentum(company_name, momentum_data):
    print("=" * 60)
    print(f"{company_name:^60}")
    print("=" * 60)

    print(f"{'First Price':30}- {momentum_data['first_price']:.2f}")
    print(f"{'Last Price':30}- {momentum_data['last_price']:.2f}")
    print(f"{'Price Change':30}- {momentum_data['price_change']:.2f}")
    print(f"{'Annual Return':30}- {momentum_data['annual_return']:.2f}")
    print("\nMonthly Returns")
    print("-" * 60)
    for month, value in momentum_data["monthly_returns"].items():
        print(f"{month:30}- {value:.2f}%")

    print("\nQuarterly Returns")
    print("-" * 60)
    for quarter, value in momentum_data["quarterly_returns"].items():
        print(f"{quarter:30}- {value:.2f}%")

def companies_annualreturn_ranking(momentum_result):
    ranking = sorted(
        momentum_result.items(),
        key = lambda item : item[1]["annual_return"],
        reverse = True
    )

    print("\n" + "=" * 60)
    print(f"{'ANNUAL RETURN RANKING':^60}")
    print("=" * 60)

    for rank,(company,data) in enumerate(ranking,start=1):
        print(
            f"{rank:02}. {company:20}"
            f"{data["annual_return"]:.2f}%"
        )