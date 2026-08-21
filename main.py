from src import (
    loader,
    stock_statistics,
    returns,
    trend,
    risk,
    momentum,
    volume,
    price_action,
    monthly,
    quarterly,
    ranking,
    signals,
    reports,
)
import sys

if __name__ == "__main__":

    folder = "data"

    stocks = loader.load_companies(folder)

    if not stocks:
        print("No company data loaded.")
        sys.exit(1)
    trend_result = {}
    stock_statistics_result = {}
    momentum_result = {}
    risk_result = {}
    volume_result = {}
    for company, stock in stocks.items():

        closing_stats = stock_statistics.company_statistics(stock)
        if closing_stats is None:
            print(f"No Closing Data Available for {company}")
        else:
            stock_statistics_result[company] = closing_stats
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

        risk_data = risk.calculate_risk(stock, company_returns["daily_returns"])
        if risk_data is None:
            print(f"No Return Data Available for {company}")
        else:
            risk_result[company] = risk_data
            risk.display_risk(company, risk_data)

        momentum_data = momentum.calculate_momentum(stock)
        if momentum_data is None:
            print(f"No Momentum Data Available for {company}")
        else:
            momentum_result[company] = momentum_data
            momentum.display_momentum(company, momentum_data)

        volume_data = volume.calculate_volume(stock)
        if volume_data is None:
            print(f"No Volume Data Available for {company}")
        else:
            volume_result[company] = volume_data
            volume.display_volume_analysis(company, volume_data)

        price_action_data = price_action.calculate_action(stock)
        if price_action_data is None:
            print(f"No Price Action Data available for {company}")
        else:
            price_action.display_price_action(company, price_action_data)

        monthly_data = monthly.calculate_monthly_analytics(stock)
        if monthly_data is None:
            print(f"No Monthly Data available for {company}")
        else:
            monthly.display_monthly(company, monthly_data)

        quarterly_data = quarterly.calculate_quarterly_analytics(stock)
        if quarterly_data is None:
            print(f"No Quarterly Data available for {company}")
        else:
            quarterly.display_quarterly_analytics(company, quarterly_data)

        signal_data = signals.generate_ma_signals(stock)
        if signal_data is None:
            print(f"Not enough data to calculate signals for {company}")
        else:
            signals.display_signals(company, signal_data)

        reports.generate_company_reports(
            company_name=company,
            stats_data=closing_stats,
            risk_data=risk_data,
            trend_data=trend_data,
            signal_data=signal_data,
        )

    trend.trend_strength_ranking(trend_result)

    annual_return_ranking_data = ranking.rank_by_annual_return(momentum_result)
    ranking.display_rank_by_annual_return(annual_return_ranking_data)

    annual_volatily_ranking_data = ranking.rank_by_annual_volatility(risk_result)
    ranking.display_rank_by_annual_volatility(annual_volatily_ranking_data)

    annual_volume_ranking_data = ranking.rank_by_annual_volume(volume_result)
    ranking.display_rank_by_annual_volume(annual_volume_ranking_data)

    average_price_ranking_data = ranking.rank_by_average_price(stock_statistics_result)
    ranking.display_rank_by_average_price(average_price_ranking_data)

    comparison_data = ranking.create_comparison_data(
        momentum_result, risk_result, volume_result
    )

    overall_ranking = ranking.calculate_overall_ranking(comparison_data)

    ranking.display_overall_company_ranking(overall_ranking)
