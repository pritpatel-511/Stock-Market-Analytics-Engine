from src import loader, stock_statistics, returns, trend, risk, momentum, volume
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
        if closing_stats is None:
            print(f"No Closing Data Available for {company}")
        else:
            stock_statistics.display_statistics(company, closing_stats)

        company_returns = returns.stock_returns(stock)
        if company_returns is None:
           print(f"No Closing Data Available for {company}") 
        else:
            returns.display_returns(company, company_returns)

        trend_data = trend.trend_analyze(stock)
        trend_result[company] = trend_data
        if trend_data is None:
            print(f"No Closing Data Available for {company}")
        else:
            trend.display_trend(company, trend_data)

        risk_result = risk.calculate_risk(stock, company_returns["daily_returns"])
        if risk_result is None:
            print(f"No Return Data Available for {company}")
        else:
            risk.display_risk(company, risk_result)

        momentum_data = momentum.calculate_momentum(stock)
        momentum_result[company] = momentum_data
        if momentum_data is None:
            print(f"No Momentum Data Available for {company}")
        else:
            momentum.display_momentum(company,momentum_data)

        volume_data = volume.calculate_volume(stock)
        if volume_data is None:
            print(f"No Volume Data Available for {company}")
        else:
            volume.display_volume_analysis(company,volume_data)
    
    trend.trend_strength_ranking(trend_result)
    momentum.companies_annualreturn_ranking(momentum_result)