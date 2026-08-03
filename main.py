from src import loader,stock_statistics
import sys

if __name__ == "__main__":

    folder = "data"

    stocks = loader.load_companies(folder)

    if not stocks:
        print("No company data loaded.")
        sys.exit(1)

    for company, stock in stocks.items():
        closing_stats = stock_statistics.company_statistics(stock)
        stock_statistics.display_statistics(company,closing_stats)
        