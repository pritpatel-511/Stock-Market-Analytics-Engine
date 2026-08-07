from src import loader, stock_statistics, returns, trend, risk
import sys

if __name__ == "__main__":

    folder = "data"

    stocks = loader.load_companies(folder)

    if not stocks:
        print("No company data loaded.")
        sys.exit(1)
    trend_result = {}
    for company, stock in stocks.items():
        closing_stats = stock_statistics.company_statistics(stock)
        stock_statistics.display_statistics(company, closing_stats)
        company_returns = returns.stock_returns(stock)
        returns.display_returns(company, company_returns)

        trend_data = trend.trend_analyze(stock)
        trend_result[company] = trend_data
        trend.display_trend(company, trend_data)

        risk_result = risk.calculate_risk(stock, company_returns["daily_returns"])
        risk.display_risk(company, risk_result)

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
