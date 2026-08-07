from src import loader, stock_statistics, returns, trend, risk, momentum
import sys

if __name__ == "__main__":

    folder = "data"

    stocks = loader.load_companies(folder)

    if not stocks:
        print("No company data loaded.")
        sys.exit(1)
    trend_result = {}
    momentum_result = {}
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

        momentum_data = momentum.calculate_momentum(stock)
        momentum_result[company] = momentum_data
        momentum.display_momentum(company,momentum_data)
    
    trend.trend_strength_ranking(trend_result)
    momentum.companies_annualreturn_ranking(momentum_result)