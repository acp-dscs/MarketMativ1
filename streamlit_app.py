# Initialise variables 
import streamlit as st
import psycopg2 as psql
import pandas as pd
from datetime import date, timedelta
from plotly import graph_objs as go

# Digital Assets Dictionary of Images and extra info for user
crypto_data = [
    {"ticker": "BTC-USD", "name": "Bitcoin", "max_supply": "21,000,000",
      "description": "Often referred to as Digital Gold. A pioneer crypto using blockchain for decentralised digital currency without intermediaries.",
        "image": "https://assets.coingecko.com/coins/images/1/standard/bitcoin.png?1696501400"},
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
      "description": "Privacy-focused fork of the Bitcoin blockchain, enables public and private transactions.",
        "image": "https://assets.coingecko.com/coins/images/486/standard/circle-zcash-color.png?1696501740"}
]
crypto_dict = {crypto['ticker']: crypto for crypto in crypto_data}

# MarketMati Streamlit Program Main Code
# Import and display logo MarketMati images from GitHub URL
mme_url = 'https://raw.githubusercontent.com/acp-dscs/MarketMativ1/main/assets/MMEYE.png'
st.image(mme_url, use_column_width=True)

# For Streamlit .TOML secrets file this replaces the .env method
marketmati = st.secrets['MARKETMATI']
host = st.secrets['HOST']
sql_password = st.secrets['SQL_PASSWORD']
db_user = st.secrets['DB_USER']
port = st.secrets['PORT']

# Function to establish connection to PostgreSQL DB
def get_db_connection():
    conn = psql.connect(
        database="pagila",
        user=db_user,
        host=host,
        password=sql_password,
        port=port
    )
    return conn

# Fetch cp_data from the database table de10_acp_mm_cp
def fetch_cp_data():
    conn = get_db_connection()
    query = "SELECT * FROM de10_acp_mm_cp"  # Select all columns from the table
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Current Prices Table
st.markdown('<h1 style="color: green;">Live Prices</h1>', unsafe_allow_html=True)
st.write('Accurate to 15 minutes')

# Transform Current Price data
cp_data = fetch_cp_data()
cp_data_renamed = cp_data[['ticker', 'current_price']].rename(columns={
    'ticker': 'Digital Asset',
    'current_price': 'Price USD'
})
# Transpose the Current Price DataFrame
cp_data_transposed = cp_data_renamed.T
st.dataframe(cp_data_transposed, hide_index=True)
# Allow user to view underlying data
if st.checkbox('Expand Current Price Table Data', key='checkbox_raw_cp_data'):
    st.write(cp_data)

# Fetch last updated rows in hp_data from the database table de10_acp_mm_hp
def fetch_hp_data():
    conn = get_db_connection()
    query = "SELECT * FROM de10_acp_mm_hp ORDER BY date_price DESC LIMIT 10"  # Fetch the last 10 rows based on timestamp
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch hp_data from the database table de10_acp_mm_hp, change INTERVAL '10 years' to number of years desired
@st.cache_data
def fetch_data():
    conn = get_db_connection()
    query = """
        SELECT *
        FROM de10_acp_mm_hp
        WHERE date_price >= NOW() - INTERVAL '10 years'
        ORDER BY date_price DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df['date_price'] = pd.to_datetime(df['date_price']).dt.tz_localize(None)
    return df

# Transform Previous Day Prices Table
st.markdown('<h1 style="color: green;">Previous Day Market Prices USD</h1>', unsafe_allow_html=True)
yesterday = date.today() - timedelta(days=1)
st.write(f'Updated daily, end of day prices for {yesterday}')
hp_data = fetch_hp_data()
hp_data_renamed = hp_data[['ticker', 'open_price', 'close_price', 'high_price', 'low_price']].rename(columns={
    'ticker': 'Digital Asset',
    'open_price': 'Open',
    'close_price': 'Close',
    'high_price': 'High',
    'low_price': 'Low'
})
st.dataframe(hp_data_renamed, hide_index=True)
# Allow user to view underlying data
if st.checkbox('Expand Open and Close Table Data', key='checkbox_raw_hp_data'):
    st.write(hp_data)

# Interactive section for user
st.markdown('<h1 style="color: green;">Cryptocurrency Deep Dive</h1>', unsafe_allow_html=True)
st.subheader('Top Picks and Analysis')
# Define data to be used and unique asset tickers
data = fetch_data()
tickers = data['ticker'].unique()
# Dropdown and additional info for user to select cryptocurrency ticker
selected_ticker = st.selectbox('Cryptocurrency tickers:', tickers, key='select_ticker_dropdown')
selected_crypto = crypto_dict[selected_ticker]
st.image(selected_crypto['image'])
st.subheader(selected_crypto['name'])
st.write(f"Max Supply: {selected_crypto['max_supply']}")
st.text(selected_crypto['description'])
# Filter by selected ticker and sort by date
filtered_data = data[data['ticker'] == selected_ticker]
filtered_data = filtered_data.sort_values('date_price')
# Calculate 111 day and 350 day simple moving averages needed for Pi Cycle
filtered_data['111SMA'] = filtered_data['close_price'].rolling(window=111, min_periods=1).mean()
filtered_data['350SMA'] = filtered_data['close_price'].rolling(window=350, min_periods=1).mean()
filtered_data['PiCycle'] = filtered_data['350SMA'] * 2
# Historical Prices and Pi Cycle Chart
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data['date_price'], y=filtered_data['close_price'], name=f"{selected_ticker} Day Close", line=dict(color='green', width=1.5)))
    fig.add_trace(go.Scatter(x=filtered_data['date_price'], y=filtered_data['111SMA'], name='111-day SMA', line=dict(color='blue', width=1.5)))
    fig.add_trace(go.Scatter(x=filtered_data['date_price'], y=filtered_data['PiCycle'], name='350-day SMA', line=dict(color='red', width=1.5)))
    fig.layout.update(title_text=f"{selected_ticker} Price with Pi Cycle Indicator", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
plot_raw_data()
# Allow user to view underlying data
if st.checkbox('Expand Chart Data', key='checkbox_raw_filtered_data'):
    st.write(filtered_data)

# Calculate and display with Plotyl Chart monthly percentage changes, use end of month close price
columns_to_drop = ['open_price', 'high_price', 'low_price', '111SMA', '350SMA', 'PiCycle']
filtered_data_subset = filtered_data.drop(columns=columns_to_drop)
monthly_last_rows = filtered_data_subset.groupby(filtered_data_subset['date_price'].dt.to_period('M')).last().reset_index(drop=True)
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
        month = row['date_price'].strftime('%Y-%m')
        change = row['month_percentage_change']
        if not pd.isnull(change):
            colour = colour_neg_red(change)
            fig.add_trace(go.Bar(
                x=[month],
                y=[change],
                marker_color=colour,
                name=row['date_price'].strftime('%b %Y'),
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

# Import and display logo MarketMati images from GitHub URL
mmf_url = 'https://raw.githubusercontent.com/acp-dscs/MarketMativ1/main/assets/MarketMati.png'
st.image(mmf_url, use_column_width=True)
# Disclaimer
st.title('')
st.markdown('<h1 style="color: red;">DISCLAIMER - MarketMati</h1>', unsafe_allow_html=True)
st.subheader('IS NOT INVESTMENT ADVICE')
st.write('Use for educational purposes only. Financial investment decisions are your own.')
st.write('**CAUTION: The Digital Assets class is highly volatile.**')
st.write('If you are considering investing in Digital Assets, ensure you **ALWAYS** seek professional advice from a qualified financial advisor.')