import sys
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


def main():
    print("Loading Data ANd Calculating Market Metrics... Please Wait.")
    folder = "data"
    stocks = loader.load_companies(folder)

    if not stocks:
        print("No company data loaded.")
        sys.exit(1)

    # --- PRE-CALCULATE ALL DATA SILENTLY ---
    # We store the results in dictionaries so we can access them instantly later
    stock_statistics_result = {}
    returns_result = {}
    risk_result = {}
    trend_result = {}
    momentum_result = {}
    volume_result = {}
    price_action_result = {}
    monthly_result = {}
    quarterly_result = {}
    signal_result = {}

    for company, stock in stocks.items():
        # 1. Statistics
        closing_stats = stock_statistics.company_statistics(stock)
        if closing_stats:
            stock_statistics_result[company] = closing_stats

        # 2. Returns & Risk
        company_returns = returns.stock_returns(stock)
        if company_returns:
            returns_result[company] = company_returns
            risk_data = risk.calculate_risk(stock, company_returns["daily_returns"])
            risk_result[company] = risk_data

        # 3. Trend
        trend_data = trend.trend_analyze(stock)
        if trend_data:
            trend_result[company] = trend_data

        # 4. omentum and Volume
        momentum_data = momentum.calculate_momentum(stock)
        if momentum_data:
            momentum_result[company] = momentum_data

        volume_data = volume.calculate_volume(stock)
        if volume_data:
            volume_result[company] = volume_data

        # 5. Price Action Data
        price_action_data = price_action.calculate_action(stock)
        if price_action_data:
            price_action_result[company] = price_action_data

        # 6. Monthly & Quarterly
        monthly_data = monthly.calculate_monthly_analytics(stock)
        if monthly_data:
            monthly_result[company] = monthly_data

        quarterly_data = quarterly.calculate_quarterly_analytics(stock)
        if quarterly_data:
            quarterly_result[company] = quarterly_data

        # 7. Signals
        signal_data = signals.generate_ma_signals(stock)
        if signal_data:
            signal_result[company] = signal_data

    # Calculating Market Ranking Silently
    comparison_data = ranking.create_comparison_data(
        momentum_result, risk_result, volume_result
    )
    overall_ranking = ranking.calculate_overall_ranking(comparison_data)
    annual_return_ranking_data = ranking.rank_by_annual_return(momentum_result)
    annual_volatily_ranking_data = ranking.rank_by_annual_volatility(risk_result)
    annual_volume_ranking_data = ranking.rank_by_annual_volume(volume_result)
    average_price_ranking_data = ranking.rank_by_average_price(stock_statistics_result)

    while True:
        print("\n" + "=" * 60)
        print(" 🚀 STOCK MARKET ANALYTICS ENGINE — MAIN MENU ")
        print("=" * 60)
        print("1. View Market Ranking Dashboard")
        print("2. Analyze a Specific Stock(Deep Dive)")
        print("3. Generate All Reports & Market Summary")
        print("4. Exit")
        print("=" * 60)

        choice = input("Enter Your Choice (1-4) : ").strip()

        if choice == "1":
            print("\n" + "=" * 60)
            print(" 📊 FULL MARKET RANKINGS DASHBOARD ")
            print("=" * 60)

            # Display All Ranking
            ranking.display_overall_company_ranking(overall_ranking)
            ranking.display_rank_by_annual_return(annual_return_ranking_data)
            ranking.display_rank_by_annual_volatility(annual_volatily_ranking_data)
            ranking.display_rank_by_annual_volume(annual_volume_ranking_data)
            ranking.display_rank_by_average_price(average_price_ranking_data)
            trend.trend_strength_ranking(trend_result)

            # Pause so the user can read the data before the menu reprints
            input("Press Enter to return to the main menu...")

        elif choice == "2":
            print("\nAvailable Companies:")
            for comp in stocks.keys():
                print(f" - {comp}")

            target = input("\n Enter Company Name to Analyze : ").strip()

            if target in stocks:
                # --- NEW MASTER HEADER ---
                print("\n" + "═" * 60)
                print(f" {target.upper()} - COMPREHENSIVE DEEP DIVE ".center(60, " "))
                print("═" * 60)

                # check and display each module if data exists
                if target in stock_statistics_result:
                    stock_statistics.display_statistics(stock_statistics_result[target])
                if target in returns_result:
                    returns.display_returns(returns_result[target])
                if target in trend_result:
                    trend.display_trend(trend_result[target])
                if target in risk_result:
                    risk.display_risk(risk_result[target])
                if target in momentum_result:
                    momentum.display_momentum(momentum_result[target])
                if target in volume_result:
                    volume.display_volume_analysis(volume_result[target])
                if target in price_action_result:
                    price_action.display_price_action(price_action_result[target])
                if target in monthly_result:
                    # print(monthly_data)
                    monthly.display_monthly(monthly_result[target])
                if target in quarterly_result:
                    quarterly.display_quarterly_analytics(quarterly_result[target])
                if target in signal_result:
                    signals.display_signals(signal_result[target])

                input("\nPress Enter to return to the main menu...")
            else:
                print(f"\n❌ Company '{target}' not found. Please check the spelling.")

        elif choice == "3":
            print("\nGenerating all individual reports and market summary...")

            # Generate individual company reports
            for company, stock in stocks.items():
                reports.generate_company_reports(
                    company_name=company,
                    stats_data=stock_statistics_result.get(company),
                    risk_data=risk_result.get(company),
                    trend_data=trend_result.get(company),
                    signal_data=signal_result.get(company),
                )

            # Generate master summary
            reports.generate_market_summary(
                overall_ranking=overall_ranking,
                return_ranking=annual_return_ranking_data,
                risk_ranking=annual_volatily_ranking_data,
            )
            print("✅ All reports successfully saved in the 'reports' folder!")

        elif choice == "4":
            print("\nExiting Engine. Goodbye!")
            break

        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
