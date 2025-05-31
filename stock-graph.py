import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

from draggable_charts import line_chart

st.title("Global Stock Market Price History")

df = yf.download([
    "BRK-A", "SE", "MCD", "NVR", "ALB", "AMZN", "SHOP", "GOOGL", "GOOG",
    "MCHP", "ILMN", "ISRG", "ADI", "AZO", "FIS", "LRCX", "MDLA", "NOW",
    "RMD", "SNPS", "VRTX", "XLNX", "YUM", "ZBRA", "ZS", "NFLX", "TSLA",
    "AMGN", "BIIB", "COST", "CSX", "DE", "DHR", "FISV", "GILD", "HCA",
    "HOLX", "KHC", "KSU", "LHX", "MCK", "MKTX", "MNST", "MRVL", "MU",
    "NXPI", "PAYX", "PCAR", "PYPL", "REGN", "SBUX", "SNOW", "SPLK",
    "TFX", "VRSK", "WBA", "ZTS"], start="2020-01-01", end="2025-01-01")
df = df.reset_index()

choose_stock = st.selectbox("Choose a stock:", [
    "BRK-A", "SE", "MCD", "NVR", "ALB", "AMZN", "SHOP", "GOOGL", "GOOG",
    "MCHP", "ILMN", "ISRG", "ADI", "AZO", "FIS", "LRCX", "MDLA", "NOW",
    "RMD", "SNPS", "VRTX", "XLNX", "YUM", "ZBRA", "ZS", "NFLX", "TSLA",
    "AMGN", "BIIB", "COST", "CSX", "DE", "DHR", "FISV", "GILD", "HCA",
    "HOLX", "KHC", "KSU", "LHX", "MCK", "MKTX", "MNST", "MRVL", "MU",
    "NXPI", "PAYX", "PCAR", "PYPL", "REGN", "SBUX", "SNOW", "SPLK",
    "TFX", "VRSK", "WBA", "ZTS"])

if choose_stock:

    chart_data = pd.DataFrame({
        "Stock": [choose_stock] * len(df),
        "Price": df["Close"][choose_stock].round(2),
        "Volume": df["Volume"][choose_stock],
        "Date": df["Date"].dt.date
    })

    st.subheader("Global Stock Graph 1-1")

    st.line_chart(chart_data.set_index("Date")["Price"])
    st.dataframe(chart_data[["Stock", "Price", "Volume", "Date"]])

    new_row_global = pd.DataFrame({
        "Stock": [choose_stock],
        "Price": [None],
        "Volume": [None],
        "Date": [None]
    })
    
    stock_randomizer = st.slider("Stock randomness (%)", 0, 100, 0)

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

#ChatGPT Section for draggable charts

st.subheader("Draggable & Random Stock Graph")

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
st.dataframe(draggable_line[["Stock", "Random Price", "Random Volume", "Date"]])
