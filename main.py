from src import loader
import sys

if __name__ == "__main__":

    folder = "data"

    stocks = loader.load_companies(folder)

    if not stocks:
        print("No company data loaded.")
        sys.exit(1)

    for company, stock in stocks.items():

        print(f"\n{'='*50}")
        print(f"Company : {company}")
        print(f"{'='*50}")

        loader.dataset_summary(stock["summary"])

        print("\nFirst 5 Dates:")
        print(stock["dates"][:5])

        print("\nFirst 5 Open Prices:")
        print(stock["open"][:5])

        print("\nFirst 5 Close Prices:")
        print(stock["close"][:5])