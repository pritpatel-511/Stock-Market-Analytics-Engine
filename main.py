from src import loader,stock_statistics,returns,trend
import sys

if __name__ == "__main__":

    folder = "data"

    stocks = loader.load_companies(folder)

    if not stocks:
        print("No company data loaded.")
        sys.exit(1)

    for company, stock in stocks.items():
        closing_stats = stock_statistics.company_statistics(stock)
        # stock_statistics.display_statistics(company,closing_stats)
        company_returns = returns.stock_returns(stock)
        # returns.display_returns(company,company_returns)
        trend_data = trend.trend_analyze(stock)
        trend.display_trend(company,trend_data)