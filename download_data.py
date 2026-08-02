import yfinance as yf

companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC": "HDFCBANK.NS",
    "ICICI": "ICICIBANK.NS"
}

for company, ticker in companies.items():
    print(f"Downloading {company}...")

    df = yf.download(
        ticker,
        period="1y",
        interval="1d"
    )

    df.to_csv(f"data/{company}.csv")

print("All datasets downloaded successfully!")