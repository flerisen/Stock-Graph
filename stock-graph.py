import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

from draggable_charts import line_chart

st.title("Global Stock Market Price History")

tickers = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "BRK.B", "TSLA", "UNH",
    "LLY", "JPM", "XOM", "JNJ", "V", "PG", "AVGO", "MA", "HD", "CVX",
    "KO", "PEP", "WMT", "BAC", "CSCO", "ADBE", "CMCSA", "NFLX", "ABT", "CRM",
    "ORCL", "MRK", "TMO", "INTC", "ACN", "COST", "MCD", "DHR", "AMD", "NEE",
    "DIS", "IBM", "TXN", "LIN", "PM", "NKE", "QCOM", "AMGN", "HON", "UNP",
    "MDT", "GE", "UPS", "LOW", "SBUX", "CAT", "GS", "INTU", "BLK", "ISRG",
    "CVS", "MS", "AMAT", "CI", "VRTX", "BA", "DE", "NOW", "LMT", "ADI",
    "T", "SYK", "ZTS", "PFE", "SPGI", "MO", "PLD", "ELV", "EL", "BDX",
    "BKNG", "MMC", "SO", "GILD", "AXP", "ADP", "C", "TJX", "REGN", "CL",
    "DUK", "BSX", "FDX", "APD", "ETN", "PNC", "EOG", "GM", "ITW", "CB",
    "USB", "FIS", "WM", "SCHW", "NSC", "EW", "TGT", "AON", "MDLZ", "HUM",
    "PGR", "FISV", "CME", "TRV", "MET", "AEP", "PSA", "SHW", "ICE", "MCO",
    "D", "EMR", "ROST", "ECL", "AIG", "MAR", "MPC", "ALL", "ORLY", "KMB",
    "STZ", "SRE", "WELL", "HCA", "CTAS", "LRCX", "IDXX", "NOC", "WMB", "CMG",
    "ADSK", "NEM", "DLR", "O", "AFL", "TEL", "CDNS", "PCAR", "SPG", "PH",
    "VLO", "FTNT", "PSX", "MNST", "CTSH", "KLAC", "ROP", "KHC", "EXC", "PAYX",
    "HPQ", "MSI", "BAX", "WEC", "AZO", "HES", "PRU", "MCK", "VRSK", "DOW",
    "PEG", "SYY", "DG", "WBA", "CMI", "MTD", "TT", "CHD", "XYL", "ZBH",
    "ED", "NUE", "CNC", "KEYS", "WST", "AMP", "HAL", "ANET", "AVB", "FTV",
    "F", "PPG", "STT", "RSG", "DLTR", "MLM", "TSCO", "LEN", "EIX", "CARR",
    "FAST", "GWW", "VFC", "IFF", "BKR", "A", "HIG", "CTVA", "DHI", "HOLX",
    "AKAM", "ALB", "PPL", "DTE", "ETR", "LUV", "VTR", "EXR", "CNP", "NTRS",
    "ES", "NTAP", "CMS", "HPE", "FMC", "DRI", "EFX", "AEE", "WAT", "NDAQ",
    "ZBRA", "ATO", "SWK", "EQR", "MTB", "GLW", "NVR", "HBAN", "RMD", "PWR",
    "TSN", "VMC", "KMI", "GRMN", "LHX", "STX", "DOV", "SJM", "MKC", "ARE",
    "ALGN", "CHRW", "KDP", "GPC", "BXP", "NDSN", "JKHY", "ESS", "UDR", "PKI",
    "INCY", "CINF", "COO", "BHF", "FRC", "PKG", "MAS", "AIZ", "CF", "HII",
    "L", "WRB", "NRG", "BBY", "AVY", "CE", "TYL", "EXPD", "IP", "HWM",
    "ROL", "OMC", "NWL", "LKQ", "WHR", "XRAY", "MOS", "APA", "UHS", "CAG",
    "EMN", "DVA", "AAL", "TPR", "NCLH", "ALLE", "FRT", "HAS", "SEE", "BEN",
    "IVZ", "RL", "DXC", "NLSN", "FLIR", "HRB", "TAP", "NWSA", "NWS", "PVH",
    "LB", "FOX", "FOXA", "HBI", "MHK", "LEG", "DISCA", "DISCK", "KSS", "GPS",
    "JWN", "UA", "UAA", "ADS", "CPB", "NBL", "HFC", "NOV", "CXO", "DVN",
    "MRO", "OKE", "XEC", "COG", "FANG", "PXD", "EQT", "SWN", "RRC", "AR",
    "CNX", "SM", "CPE", "MTDR", "CRK", "PDCE", "LPI", "OXY", "CLR", "WLL"]

choose_stock = st.selectbox("Choose a stock:", tickers)

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(url)
sp500_table = tables[0]
ticker_to_name = dict(zip(sp500_table['Symbol'], sp500_table['Security']))
df['Company Name'] = df['Symbol'].map(ticker_to_name)

df_all = yf.download(tickers, start="2020-01-01", end="2025-01-01", group_by="ticker")
df_all = df.reset_index()

stock_df = df_all[choose_stock].copy()
stock_df = stock_df.reset_index()
stock_df['Symbol'] = choose_stock
stock_df['long_name'] = ticker_to_name.get(choose_stock, "Unknown")

if choose_stock:
    chart_data = pd.DataFrame({
        "type": ["Stock"] * len(stock_df),
        "challenge_id": st.number_input("Input a challenge_id", value=0),
        "Name": [choose_stock] * len(stock_df),
        "long_name": [ticker_to_name.get(choose_stock, "Unknown")] * len(stock_df),
        "Price": stock_df["Close"][choose_stock].round(2),
        "Volume": stock_df["Volume"][choose_stock],
        "Date": stock_df["Date"].dt.date
    })
    
    st.subheader("Global Stock Graph 1-1")

    st.line_chart(chart_data.set_index("Date")["Price"])
    st.dataframe(chart_data[["type", "challenge_id","Name","long_name", "Price", "Volume", "Date"]])

    new_row_global = pd.DataFrame({
        "Stock": [choose_stock],
        "Price": [None],
        "Volume": [None],
        "Date": [None]
    })

#ChatGPT Section for draggable charts

st.subheader("Draggable & Random Stock Graph")

#Stock randomizer part
stock_randomizer = st.slider("Stock randomness (%)", 1, 100, 1)

if stock_randomizer != 0:
    price_multiplier = 1 + (stock_randomizer / 100)
    np.random.seed(42)
    noise = np.random.normal(loc=1.0, scale=0.01, size=len(chart_data))

    chart_data["Random Price"] = (
        chart_data["Price"] * price_multiplier * noise
    ).round(2)

    chart_data["Random Volume"] = (
        chart_data["Volume"] * (1 + stock_randomizer / 200)
    ).astype(int)

# Prepare yearly aggregated data for the draggable chart (average price and volume)
draggable_line = chart_data.copy()
draggable_line["Year"] = pd.to_datetime(draggable_line["Date"]).dt.year
yearly_data = draggable_line.groupby("Year")[["Random Price", "Random Volume"]].mean()

# Reset index so 'Year' is a column
yearly_data = yearly_data.reset_index()

# Use string year for draggable chart's index (needed for JSON serialization)
draggable_line_yearly = yearly_data.copy()
draggable_line_yearly["Year"] = draggable_line_yearly["Year"].astype(str)
draggable_line_yearly = draggable_line_yearly.set_index("Year")

updated_data = line_chart(data=draggable_line_yearly, options={
    "title": f"Draggable chart: {choose_stock}",
    "x_label": "Year",
    "y-label": "Value",
    "x_grid": True,
    "y_grid": True,
    "tension": 0,
}, key="draggable_chart")

# Convert updated_data back to DataFrame
updated_yearly_data = updated_data.copy()
updated_yearly_data = updated_yearly_data.reset_index()

# Rename 'index' to 'Year' if needed
if 'Year' not in updated_yearly_data.columns and 'index' in updated_yearly_data.columns:
    updated_yearly_data.rename(columns={'index': 'Year'}, inplace=True)

updated_yearly_data["Year"] = updated_yearly_data["Year"].astype(int)

# Merge updated yearly price and volume back into the daily data
draggable_line = draggable_line.merge(
    updated_yearly_data[["Year", "Random Price", "Random Volume"]],
    on="Year",
    suffixes=("", "_updated")
)

# Create dicts for year to updated values
year_price_dict = updated_yearly_data.set_index('Year')['Random Price'].to_dict()
year_volume_dict = updated_yearly_data.set_index('Year')['Random Volume'].to_dict()
years_sorted = sorted(year_price_dict.keys())

interpolated_prices = []
interpolated_volumes = []

for i, year in enumerate(years_sorted):
    price_start = year_price_dict[year]
    price_end = year_price_dict[years_sorted[i+1]] if i+1 < len(years_sorted) else price_start

    volume_start = year_volume_dict[year]
    volume_end = year_volume_dict[years_sorted[i+1]] if i+1 < len(years_sorted) else volume_start

    mask = draggable_line['Year'] == year
    days_in_year = mask.sum()

    if days_in_year > 1:
        interpolated_price = np.linspace(price_start, price_end, days_in_year)
        interpolated_volume = np.linspace(volume_start, volume_end, days_in_year)
    else:
        interpolated_price = np.array([price_start])
        interpolated_volume = np.array([volume_start])

    interpolated_prices.extend(interpolated_price)
    interpolated_volumes.extend(interpolated_volume)

# Assign the interpolated values back and round
draggable_line.loc[:, 'Random Price'] = interpolated_prices
draggable_line.loc[:, 'Random Volume'] = interpolated_volumes
draggable_line['Random Price'] = draggable_line['Random Price'].round(2)
draggable_line['Random Volume'] = draggable_line['Random Volume'].round(2)

# Drop helper columns
draggable_line = draggable_line.drop(columns=["Random Price_updated", "Random Volume_updated"])

# Show the updated daily data with smooth prices and volumes
st.dataframe(draggable_line[["type", "challenge_id","Name","long_name", "Random Price", "Random Volume", "Date"]])
