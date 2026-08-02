import csv
from datetime import datetime
import numpy as np
import os

def validate_date(date):
    try:
        datetime.strptime(date,"%Y-%m-%d")
        return True
    except ValueError:
        return False
def validate_row(row):
    """
    Validate a single row of stock data.

    Returns:
        (True, "") if valid
        (False, reason) if invalid
    """

    if len(row) != 6:
        return False,"Incorrect Number of Columns"
    
    date  = row[0]
    
    if not validate_date(date):
        return False,f"Invalid Date {date}"

    try:
        open_price = float(row[1])
        high_price = float(row[2])
        low_price = float(row[3]) 
        close_price = float(row[4])
        volume = int(float(row[5]))
    except ValueError:
        return False,"Invalid numeric Value"

    #negative Value
    if (open_price < 0
    or high_price < 0
    or low_price < 0
    or close_price < 0
    ):
        return False,"Negative Price Found"
    
    #Finanacial Validation

    if low_price > high_price:
        return False,"Low > High"
    
    if open_price > high_price:
        return False,"Open > High"

    if open_price < low_price:
        return False,"Open < Low"

    if close_price > high_price:
        return False,"Close > High"

    if close_price < low_price:
        return False,"Close < Low"

    return True,""

def load_csv(filename):
    dates = []
    open_price = []
    high_price = []
    low_price = []
    close_price = []
    volume = []
    
    unique_dates = set()
    
    total_row = 0
    valid_row = 0
    invalid_row = 0

    try:  
        with open(filename,"r",encoding="utf-8") as file:
            reader = csv.reader(file)
            
            #skip header
            header = next(reader,None)

            if header is None:
                print("CSV File is completely empty.")
                return None
            
            for row in reader :
                total_row += 1
                
                
                valid,reason = validate_row(row)
                
                if not valid:
                    invalid_row += 1
                    print(f"Skipping Row {total_row} : {reason}")
                    continue
                
                date = row[0].strip()

                if date in unique_dates:
                    invalid_row += 1
                    print(f"Duplicate Date Found : {date}")
                    continue

                unique_dates.add(date)

                dates.append(date)
                open_price.append(float(row[1]))
                high_price.append(float(row[2]))
                low_price.append(float(row[3]))
                close_price.append(float(row[4]))
                volume.append(int(float(row[5])))

                valid_row += 1
            if total_row == 0:
                    print("CSV file containes only header and no data.")
                    return None

    except FileNotFoundError:
        print(f"File{filename} Not found.")

    dates = np.array(dates)
    open_price = np.array(open_price)
    high_price = np.array(high_price)
    low_price = np.array(low_price)
    close_price = np.array(close_price)
    volume = np.array(volume)

    summary = {
        "total_rows" : total_row,
        "valid_rows" : valid_row,
        "invalid_rows" : invalid_row,
        "unique_dates" : len(unique_dates)
    }
    return {
        "dates":dates,
        "open":open_price,
        "high":high_price,
        "low":low_price,
        "close":close_price,
        "volume":volume,
        "summary":summary,
    }
    

def dataset_summary(summary):
    print("\n" + "-"*40)
    print("     Dataset Summary")
    print("-"*40)

    print(f"Total Rows : {summary["total_rows"]}")
    print(f"Valid Rows : {summary["valid_rows"]}")
    print(f"Invalid Rows : {summary["invalid_rows"]}")
    print(f"Unique Dates : {summary["unique_dates"]}")

    print("-"*40)

def load_companies(folerpath):
    stock_data = {}

    files = os.listdir(folerpath)

    for file in files:
        if not file.endswith(".csv"):
            continue

        filepath = os.path.join(folerpath,file)
        company_name = file.replace(".csv","")
        stock_data[company_name] = load_csv(filepath)
    return stock_data