# Capstone Project (Data Engineering) - MarketMati

# Welcome to MarketMati
![Alt text](https://raw.githubusercontent.com/acp-dscs/MarketMativ1/main/assets/MMEYE.png)
- 👋 Hi there, this Web App will help you keep a sharp eye on the Digital Assets market!

## Description

📈 Digital Assets Current & Historical Prices
💹 Pi Cycle Analysis

With a focus on data visualisations through chart analysis.
This Webb App aims to asist in your learning and understanding of current and historical market prices.
The program has been developed with a fully operational ETL data pipeline.

## Data Flow Diagram
![Alt text](https://raw.githubusercontent.com/acp-dscs/MarketMativ1/main/assets/DataFlow.png)

## Key Processes

### Data Extraction
-     Financial Historical and Current Data from the Yfinance API.
-     https://pypi.org/project/yfinance/ 
-     Data is then stored in DBeaver Pagila SQL database tables.
-     Data is updated via automated CRON Jobs.
-     Current Prices every 15mins and Day Close Prices once a day.
### Data Transformation
-     Using Python and SQL, data tables are queried.
-     Any transformation, column renaming, dropping of data, sorting etc.
### Data Load
-     Transformed and updated data is now used to create user visualisations.
-     The Web App is hosted with Streamlit. https://streamlit.io/

📫 How to reach me at:
-     MarketMati GitHub Repo:    https://marketmativ1.streamlit.app/
-     MarketMati GitHub Repo:    https://github.com/acp-dscs/MarketMati
-     Website:                   https://anthonypieri.com/
-     LinkedIn:                  https://www.linkedin.com/in/anthonypieri/

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://data-evaluation-template.streamlit.app/)

### How to run on your own machine
1. Install the requirements
   ```
   $ pip install -r requirements.txt
   ```
2. Run the app
   ```
   $ streamlit run streamlit_app.py
   ```

![Alt text](https://raw.githubusercontent.com/acp-dscs/MarketMativ1/main/assets/MarketMati.png)

<!---
acp-dscs/acp-dscs is a ✨ special ✨ repository because its `README.md` (this file) appears on my GitHub profile.
--->
