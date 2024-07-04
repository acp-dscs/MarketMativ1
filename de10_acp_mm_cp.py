# Current Prices Code Run every 15 minutes

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

# Define the list of ticker symbols
ticker_symbols = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD",
    "ADA-USD", "DOT-USD", "LINK-USD", "MATIC-USD", "ZEC-USD"
]

# Store the current prices in a list
current_prices = []

# Fetch Digital Asset current price accurate to 1min from Yfinance
for ticker_symbol in ticker_symbols:
    ticker_data = yf.Ticker(ticker_symbol)
    hist_data = ticker_data.history(period="1d", interval="1m")
    current_price = hist_data['Close'][-1]
    current_prices.append([ticker_symbol, current_price, datetime.now()])

# Create DataFrame
prices_df = pd.DataFrame(current_prices,
                         columns=['Ticker', 'Current Price', 'Timestamp'])

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

for index, row in prices_df.iterrows():
    cur.execute(f"""
    SELECT EXISTS(SELECT 1 FROM de10_acp_mm_cp WHERE ticker = '{row['Ticker']}')
    """)
    exists = cur.fetchone()[0]

    if exists:
        sql = f"""
            UPDATE de10_acp_mm_cp
            SET current_price = {row['Current Price']}, timestamp = '{row['Timestamp']}'
            WHERE ticker = '{row['Ticker']}'
        """
    else:
        sql = f"""
            INSERT INTO de10_acp_mm_cp (ticker, current_price, timestamp)
            VALUES ('{row['Ticker']}', {row['Current Price']}, '{row['Timestamp']}')
        """

    cur.execute(sql)

# Commit and close the connection
conn.commit()
conn.close()