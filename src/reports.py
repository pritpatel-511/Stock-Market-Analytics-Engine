import os


def generate_company_reports(
    company_name, stats_data, risk_data, trend_data, signal_data, output_dir="reports"
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, f"{company_name}_Reports.txt")

    with open(file_path, "w") as file:
        # --- HEADER ---
        file.write("=" * 60 + "\n")
        file.write(f"{company_name.upper()} - COMPREHENSIVE ANALYTICS REPORT\n")
        file.write("=" * 60 + "\n\n")

        # --- SECTION 1: BASIC STATISTICS ---
        if stats_data:
            file.write("--- 1. Company Statistics---\n")
            file.write(f"{'Trading Days':30}: {stats_data['trading_days']}\n")
            file.write(f"{'Average Price':30}: {stats_data['average_price']:.2f}\n")
            file.write(f"{'Highest Price':30}: {stats_data['highest_price']:.2f}\n")
            file.write(f"{'Lowest Price':30}: {stats_data['lowest_price']:.2f}\n")
            file.write(
                f"{'Price Volatility':30}: {stats_data['coefficient_of_variation']*100:.2f}%\n\n"
            )

        # --- SECTION 2 : RISK ENGINE ---
        if risk_data:
            file.write("--- 2. RISK ANALYSIS ---\n")
            file.write(
                f"Annualized Volatility: {risk_data['annualized_volatility'] * 100:.2f}%\n"
            )
            file.write(
                f"Maximum Drawdown:      {risk_data['maximum_drawdown'] * 100:.2f}%\n"
            )
            file.write(
                f"Max Recovery Time:     {risk_data['maximum_recovery_days']} days\n"
            )
            file.write(f"Winning Days:          {risk_data['winning_days']}\n")
            file.write(f"Losing Days:           {risk_data['losing_days']}\n")
            file.write(f"Composite Risk Score:  {risk_data['risk_score']:.2f} / 100\n")
            file.write(f"Risk Level:            {risk_data['risk_level']}\n\n")

        # --- SECTION 3: TREND ANALYSIS ---
        if trend_data:
            file.write("--- 3. TREND STRENGTH ---\n")
            file.write(f"Current Trend:         {trend_data['current_trend']}\n")
            file.write(f"Bullish Days:          {trend_data['bullish_days']}\n")
            file.write(f"Bearish Days:          {trend_data['bearish_days']}\n")
            file.write(
                f"Trend Strength Score:  {trend_data['trend_strength_score']:.2f} / 100\n"
            )
            file.write(f"Trend Strength:        {trend_data['trend_strength']}\n\n")

        # --- SECTION 4: INVESTMENT SIGNALS ---
        if signal_data:
            file.write(
                f"--- 4. INVESTMENT SIGNALS (MA {signal_data['short_window']}/{signal_data['long_window']}) ---\n"
            )
            file.write(f"Total BUY Signals:     {signal_data['total_buys']}\n")
            file.write(f"Total SELL Signals:    {signal_data['total_sells']}\n\n")

            file.write("Recent BUY Signals:\n")
            if signal_data["buy_signals"]:
                # Print only the last 5 buy signals to keep the report clean
                for signal in signal_data["buy_signals"][-5:]:
                    file.write(
                        f"  - Date: {signal['date']} | Price: {signal['price']:.2f}\n"
                    )
            else:
                file.write("  - No Buy Signals generated.\n")

            file.write("\nRecent SELL Signals:\n")
            if signal_data["sell_signals"]:
                for signal in signal_data["sell_signals"][-5:]:
                    file.write(
                        f"  - Date: {signal['date']} | Price: {signal['price']:.2f}\n"
                    )
            else:
                file.write("  - No Sell Signals generated.\n")

    print(f"Report Successfully Generated: {file_path}")
