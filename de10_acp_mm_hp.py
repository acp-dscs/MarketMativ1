# Daily New Historical Price Run once a day at 11:55pm

# List of imports
import yfinance as yf
import pandas as pd
import psycopg2 as psql
import os
from dotenv import load_dotenv
from datetime import datetime

# Load secrets from .env file
load_dotenv()
marketmati = os.getenv('MARKETMATI')
host = os.getenv('HOST')
sql_password = os.getenv('SQL_PASSWORD')
db_user = os.getenv('DB_USER')
port = os.getenv('PORT')

# Define list of ticker symbols
ticker_symbols = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD",
    "ADA-USD", "DOT-USD", "LINK-USD", "MATIC-USD", "ZEC-USD"
]

# Store end of day historical market price data in a list
hist_data_list = []

# Fetch Digital Asset end of day historical market price data from Yfinance
for ticker_symbol in ticker_symbols:
    ticker_data = yf.Ticker(ticker_symbol)
    hist_data = ticker_data.history(period="1d")
    # Data cleanse drop columns
    hist_data = hist_data.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1)
    hist_data['Ticker'] = ticker_symbol # Add column Asset ticker for reference
    hist_data_list.append(hist_data)

# Combine DataFrames
combined_data = pd.concat(hist_data_list)
combined_data = combined_data.reset_index()
combined_data.columns = ['date_price', 'open_price', 'high_price',
                         'low_price', 'close_price', 'ticker']

# Establish connection to PostgreSQL DB
conn = psql.connect(
    database="pagila",
    user=db_user,
    host=host,
    password=sql_password,
    port=port
)

# Enter the new data to the DB
cur = conn.cursor()

for index, row in combined_data.iterrows():
    cur.execute("SELECT MAX(unique_id) FROM de10_acp_mm_hp")
    max_unique_id = cur.fetchone()[0]
    if max_unique_id is None:
        max_unique_id = 0

    sql = f"""
        INSERT INTO de10_acp_mm_hp (unique_id, date_price, open_price, high_price, low_price, close_price, ticker)
        VALUES ({max_unique_id + 1}, '{row['date_price']}', {row['open_price']}, {row['high_price']}, {row['low_price']}, {row['close_price']}, '{row['ticker']}')
    """

    cur.execute(sql)

# Commit and close the connection
conn.commit()
conn.close()