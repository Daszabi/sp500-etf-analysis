import yfinance as yf
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def main():
    print("1. Downloading data from Yahoo Finance (BlackRock IVV ETF)...")
    # Using Ticker().history() instead of download() to guarantee a flat, bug-free column structure
    ivv_etf = yf.Ticker("IVV")
    data = ivv_etf.history(start="2021-05-27", end="2026-05-27")
    
    # Resetting the index moves the Date from the index into a standard column
    data.reset_index(inplace=True)
    
    # Ensuring the first column is strictly named 'Date' (handles 'Datetime' or 'date' variations)
    data.rename(columns={data.columns[0]: 'Date'}, inplace=True)
    
    # Selecting only the required core columns
    df_clean = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    
    # Converting Date to a standard string format ('YYYY-MM-DD') for perfect SQLite compatibility
    df_clean['Date'] = pd.to_datetime(df_clean['Date']).dt.strftime('%Y-%m-%d')

    print("2. Creating local SQL database and loading data...")
    # Creating a local SQLite database file (etf_data.db)
    conn = sqlite3.connect('etf_data.db')
    cursor = conn.cursor()
    
    # Dropping the table if it exists to avoid duplication on multiple runs, then creating a new one
    cursor.execute('DROP TABLE IF EXISTS ivv_stock_data')
    df_clean.to_sql('ivv_stock_data', conn, index=False)

    print("3. Querying data using SQL (SELECT, WHERE)...")
    # Fetching data exactly from the start date using SQL
    query = """
    SELECT Date, Close 
    FROM ivv_stock_data 
    WHERE Date >= '2021-05-27'
    ORDER BY Date ASC
    """
    # Loading the query results directly into a Pandas DataFrame
    df_sql = pd.read_sql_query(query, conn)
    conn.close()

    print("4. Quantitative analysis with Pandas (Moving Averages)...")
    # Restoring Date format to datetime for time-series analysis and plotting
    df_sql['Date'] = pd.to_datetime(df_sql['Date'])
    df_sql.set_index('Date', inplace=True)
    
    # Calculating 50-day and 200-day Moving Averages (MA)
    df_sql['MA_50'] = df_sql['Close'].rolling(window=50).mean()
    df_sql['MA_200'] = df_sql['Close'].rolling(window=200).mean()

    print("5. Generating data visualization...")
    # Plotting professional financial chart
    plt.figure(figsize=(14, 7))
    plt.plot(df_sql.index, df_sql['Close'], label='IVV Daily Close Price', color='black', alpha=0.6)
    plt.plot(df_sql.index, df_sql['MA_50'], label='50-Day Moving Average', color='blue', linewidth=2)
    plt.plot(df_sql.index, df_sql['MA_200'], label='200-Day Moving Average', color='red', linewidth=2)
    
    # Chart styling and labels
    plt.title('BlackRock iShares S&P 500 ETF (IVV) - Performance (2021 - 2026)', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Closing Price (USD)', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Saving and displaying the chart
    plt.savefig('IVV_Performance_Analysis_2021_2026.png', bbox_inches='tight')
    print("Done! Chart saved as 'IVV_Performance_Analysis_2021_2026.png'.")
    plt.show()

if __name__ == "__main__":
    main()
