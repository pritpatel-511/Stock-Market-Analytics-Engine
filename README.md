# 🚀 Stock Market Analytics Engine

A high-performance, modular Stock Market Analytics Engine built entirely in Python and NumPy. This project analyzes historical OHLCV (Open, High, Low, Close, Volume) data for multiple companies, calculating advanced financial metrics, technical indicators, and composite risk scores without relying on Pandas.

## 📊 Features

* **Advanced Risk Engine:** Calculates Annualized Volatility, Maximum Drawdown, and Recovery Time using vectorized NumPy arrays (`np.maximum.accumulate`).
* **Investment Signals:** Automatically detects and dates **Golden Cross (Buy)** and **Death Cross (Sell)** events using Moving Average crossovers.
* **Trend & Momentum Analytics:** Computes Bullish/Bearish streaks, monthly/quarterly returns, and price action metrics (gap ups, intraday ranges).
* **Multi-Company Ranking:** Automatically aggregates data from multiple CSVs and ranks stocks by Overall Score, Annual Return, and Lowest Risk.
* **Automated Reporting:** Generates clean, formatted `.txt` reports for individual companies and a master Market Summary.
* **Interactive CLI:** A sleek, user-friendly Command Line Interface for dynamic data lookup and dashboard viewing.

## 🏗️ Project Architecture

The engine is built with a strict modular architecture, keeping data loading, statistical calculations, and user interface separated.

```text
Stock-Market-Analytics-Engine/
│
├── data/                  # Drop company CSV files here (Date, Open, High, Low, Close, Volume)
├── reports/               # Auto-generated TXT reports are saved here
│
├── src/
│   ├── loader.py          # OS-level multi-file loader and data validator
│   ├── stock_statistics.py# Core price variances and percentiles
│   ├── returns.py         # Daily return calculations
│   ├── trend.py           # Moving averages and bullish/bearish scoring
│   ├── risk.py            # Drawdown and composite risk scoring
│   ├── momentum.py        # Annual returns and price change
│   ├── volume.py          # Volume spikes and growth tracking
│   ├── price_action.py    # Intraday ranges and gap analysis
│   ├── monthly.py         # Monthly aggregated metrics
│   ├── quarterly.py       # Quarterly aggregated metrics
│   ├── signals.py         # Golden/Death Cross generation
│   ├── ranking.py         # Market comparison logic
│   └── reports.py         # File I/O for TXT generation
│
├── main.py                # The interactive CLI orchestrator
├── requirements.txt
└── README.md