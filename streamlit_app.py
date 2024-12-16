import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from plotly import graph_objs as go

# Digital Assets Dictionary of Images and extra info for user
crypto_data = [
    {"ticker": "BTC-USD", "name": "Bitcoin", "max_supply": "21,000,000",
     "description": "Often referred to as Digital Gold. A pioneer crypto using blockchain for decentralised digital currency without intermediaries.",
     "image": "https://assets.coingecko.com/coins/images/1/standard/bitcoin.png?1696501400"},
     {"ticker": "MSTR", "name": "MicroStrategy", "max_supply": "Infinite",
     "description": "Bitcoin Treasury Company (BTC) In August 2020, MicroStrategy became the first publicly traded US company to acquire and hold bitcoin on its balance sheet as a primary treasury reserve asset. ",
     "image": "https://raw.githubusercontent.com/acp-dscs/MarketMativ1/main/assets/MSTR.png"},
    {"ticker": "ETH-USD", "name": "Ethereum", "max_supply": "Infinite",
     "description": "Proof-of-Stake blockchain for dApps, scaling with Layer 2 solutions.",
     "image": "https://assets.coingecko.com/coins/images/279/standard/ethereum.png?1696501628"},
    {"ticker": "BNB-USD", "name": "Binance Chain", "max_supply": "200,000,000",
     "description": "Native Binance Smart Chain coin, reduces trading fees.",
     "image": "https://assets.coingecko.com/coins/images/825/standard/bnb-icon2_2x.png?1696501970"},
    {"ticker": "SOL-USD", "name": "Solana", "max_supply": "Infinite",
     "description": "Fast Layer 1 blockchain with smart contracts, Proof-of-History and Stake.",
     "image": "https://assets.coingecko.com/coins/images/4128/standard/solana.png?1718769756"},
    {"ticker": "XRP-USD", "name": "XRP", "max_supply": "100,000,000,000",
     "description": "Facilitates global payments via XRPL ledger for banks and providers.",
     "image": "https://assets.coingecko.com/coins/images/44/standard/xrp-symbol-white-128.png?1696501442"},
    {"ticker": "ADA-USD", "name": "Cardano", "max_supply": "45,000,000,000",
     "description": "Proof-of-Stake blockchain, supports dApps, with a multi-asset ledger and smart contracts.",
     "image": "https://assets.coingecko.com/coins/images/975/standard/cardano.png?1696502090"},
    {"ticker": "DOT-USD", "name": "Polkadot", "max_supply": "Infinite",
     "description": "Builds decentralised oracle networks for secure blockchain smart contracts.",
     "image": "https://static.coingecko.com/s/polkadot-73b0c058cae10a2f076a82dcade5cbe38601fad05d5e6211188f09eb96fa4617.gif"},
    {"ticker": "LINK-USD", "name": "Chainlink", "max_supply": "1,000,000,000",
     "description": "Layer-0 platform linking chains, pooled security, diverse protocols.",
     "image": "https://assets.coingecko.com/coins/images/877/standard/chainlink-new-logo.png?1696502009"},
    {"ticker": "MATIC-USD", "name": "Polygon", "max_supply": "10,000,000,000",
     "description": "The first well-structured, easy-to-use platform for Ethereum scaling.",
     "image": "https://assets.coingecko.com/coins/images/4713/standard/polygon.png?1698233745"},
    {"ticker": "ZEC-USD", "name": "Zcash", "max_supply": "21,000,000",
     "description": "Zcash (ZEC), based on Bitcoin's codebase, uses zk-SNARKs to offer optional anonymity through shielded transactions. As the first major application of this zero-knowledge cryptography, Zcash ensures privacy by encrypting shielded transactions while still validating them under network rules.",
     "image": "https://assets.coingecko.com/coins/images/486/standard/circle-zcash-color.png?1696501740"}
]
crypto_dict = {crypto['ticker']: crypto for crypto in crypto_data}

# MarketMati Streamlit Program Main Code
mme_url = 'https://raw.githubusercontent.com/acp-dscs/MarketMativ1/main/assets/MMEYE.png'
st.image(mme_url, use_container_width=True)

# Fetch data from Yahoo Finance
def fetch_yf_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    data = data['Close'].reset_index()
    data = data.melt(id_vars=['Date'], var_name='ticker', value_name='close_price')
    return data

# Current Prices Table
st.markdown('<h1 style="color: green;">Live Prices - Select Assets</h1>', unsafe_allow_html=True)
st.write('Accurate to the latest market data')

# Fetch live prices
def fetch_live_prices(tickers):
    live_data = []
    for ticker in tickers:
        ticker_data = yf.Ticker(ticker)
        hist_data = ticker_data.history(period="1d")
        if not hist_data.empty and 'Close' in hist_data.columns:
            live_price = hist_data['Close'].iloc[-1]
            live_data.append({"ticker": ticker, "current_price": live_price})
        else:
            live_data.append({"ticker": ticker, "current_price": None})  # Handle missing data gracefully
    return pd.DataFrame(live_data)

live_prices = fetch_live_prices([crypto['ticker'] for crypto in crypto_data])
st.dataframe(live_prices.rename(columns={"ticker": "Digital Asset", "current_price": "Price USD"}), hide_index=True)

# Interactive Section for User
st.markdown('<h1 style="color: green;">Cryptocurrency Deep Dive</h1>', unsafe_allow_html=True)
st.subheader('Top Picks and Analysis')
selected_ticker = st.selectbox('Cryptocurrency tickers:', [crypto['ticker'] for crypto in crypto_data])
selected_crypto = crypto_dict[selected_ticker]
st.image(selected_crypto['image'])
st.subheader(selected_crypto['name'])
st.write(f"Max Supply: {selected_crypto['max_supply']}")
st.text(selected_crypto['description'])

# Fetch historical data
historical_data = fetch_yf_data([selected_ticker], "2010-01-01", date.today().strftime('%Y-%m-%d'))
historical_data = historical_data[historical_data['ticker'] == selected_ticker]
historical_data['111SMA'] = historical_data['close_price'].rolling(window=111, min_periods=1).mean()
historical_data['350SMA'] = historical_data['close_price'].rolling(window=350, min_periods=1).mean()
historical_data['PiCycle'] = historical_data['350SMA'] * 2

# Historical Prices and Pi Cycle Chart
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['close_price'], name=f"{selected_ticker} Day Close", line=dict(color='green', width=1.5)))
    fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['111SMA'], name='111-day SMA', line=dict(color='blue', width=1.5)))
    fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['PiCycle'], name='350-day SMA', line=dict(color='red', width=1.5)))
    fig.layout.update(title_text=f"{selected_ticker} Price with Pi Cycle Indicator", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Calculate and display with Plotly Chart monthly percentage changes, use end of month close price
columns_to_drop = ['open_price', 'high_price', 'low_price', '111SMA', '350SMA', 'PiCycle']
filtered_data_subset = historical_data.drop(columns=[col for col in columns_to_drop if col in historical_data])
monthly_last_rows = filtered_data_subset.groupby(filtered_data_subset['Date'].dt.to_period('M')).last().reset_index(drop=True)
monthly_last_rows['month_percentage_change'] = monthly_last_rows['close_price'].pct_change() * 100
def colour_neg_red(value):
    if value > 0:
        return 'green'
    elif value < 0:
        return 'red'
    else:
        return 'grey'

st.markdown('<h1 style="color: green;">Monthly Percentage Changes</h1>', unsafe_allow_html=True)

if selected_ticker:
    data_selected = monthly_last_rows[monthly_last_rows['ticker'] == selected_ticker]
    fig = go.Figure()
    for index, row in data_selected.iterrows():
        month = row['Date'].strftime('%Y-%m')
        change = row['month_percentage_change']
        if not pd.isnull(change):
            colour = colour_neg_red(change)
            fig.add_trace(go.Bar(
                x=[month],
                y=[change],
                marker_color=colour,
                name=row['Date'].strftime('%b %Y'),
                text=f"{change:.2f}%",
                hoverinfo='text'
            ))
    fig.update_layout(
        title=f'Monthly Percentage Changes for {selected_ticker}',
        xaxis_title='',
        yaxis_title='Percentage Change (%)',
        barmode='stack',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig)

# Allow user to view underlying data
if st.checkbox('Expand Monthly Percentages Data', key='checkbox_raw_monthly_last_rows'):
    st.write(monthly_last_rows)

# --- Add Annual Candlestick Section ---
# Hardcoded data for Bitcoin from 2008 to 2013
hardcoded_btc_data = {
    'Year': [2008, 2009, 2010, 2011, 2012, 2013],
    'Year Open': [0.001, 0.39, 0.10, 0.30, 5.27, 13.30],
    'Year High': [0.39, 1.00, 0.39, 31.91, 13.70, 1156.00],
    'Year Low': [0.001, 0.01, 0.06, 2.05, 4.41, 13.30],
    'Year Close': [0.39, 0.10, 0.30, 4.70, 13.30, 755.00],
    'Digital Asset': ['BTC-USD'] * 6
}

# Convert hardcoded data into a DataFrame for Bitcoin
btc_data_df = pd.DataFrame(hardcoded_btc_data)

# Fetch annual candlestick data for the selected crypto
def fetch_annual_candles(tickers, start_date="2010-01-01"):
    annual_data = []
    for ticker in tickers:
        ticker_data = yf.Ticker(ticker)  # Fetch data from Yahoo Finance
        history = ticker_data.history(start=start_date, interval="1mo")  # Fetch monthly data from start date
        history.reset_index(inplace=True)
        history['Year'] = history['Date'].dt.year  # Extract year from Date
        yearly_summary = history.groupby('Year').agg(
            Open=('Open', 'first'),
            High=('High', 'max'),
            Low=('Low', 'min'),
            Close=('Close', 'last')
        ).reset_index()
        yearly_summary['ticker'] = ticker
        annual_data.append(yearly_summary)
    return pd.concat(annual_data, ignore_index=True)

# Fetch annual candlestick data for the selected tickers
tickers = [selected_ticker]  # Only show the selected ticker in the interactive section
annual_candles_data = fetch_annual_candles(tickers, start_date="2014-01-01")

# Rename and display the dataframe with relevant columns
annual_candles_data.rename(columns={
    'ticker': 'Digital Asset',
    'Open': 'Year Open',
    'High': 'Year High',
    'Low': 'Year Low',
    'Close': 'Year Close'
}, inplace=True)

# Combine the hardcoded BTC data with the fetched data only if the selected ticker is BTC-USD
if selected_ticker == 'BTC-USD':
    combined_data = pd.concat([btc_data_df, annual_candles_data], ignore_index=True)
else:
    combined_data = annual_candles_data

# Show the full table with the annual candlestick data
st.markdown('<h2 style="color: green;">Annual Data</h2>', unsafe_allow_html=True)
st.dataframe(combined_data, hide_index=True)

# Import and display logo MarketMati images from GitHub URL
mmf_url = 'https://raw.githubusercontent.com/acp-dscs/MarketMativ1/main/assets/MarketMati.png'
st.image(mmf_url, use_container_width=True)

# Disclaimer
st.title('')
st.markdown('<h1 style="color: red;">DISCLAIMER - MarketMati</h1>', unsafe_allow_html=True)
st.subheader('IS NOT INVESTMENT ADVICE')
st.write('Use for educational purposes only. Financial investment decisions are your own.')
st.write('**CAUTION: The Digital Assets class is highly volatile.**')
st.write('If you are considering investing in Digital Assets, ensure you **ALWAYS** seek professional advice from a qualified financial advisor.')
