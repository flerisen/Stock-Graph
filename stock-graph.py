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
        "Price": df["Close"][choose_stock],
        "Volume": df["Volume"][choose_stock],
        "Date": df["Date"].dt.date
    })

    st.subheader("Global Stock Graph 1-1")

    st.line_chart(chart_data.set_index("Date")["Price"])
    st.dataframe(chart_data[["Stock", "Price", "Volume", "Date"]])

    st.subheader("Stock Randomness Graph")

    stock_randomizer = st.slider("Stock randomness (%)", 0, 100, 0)

    chart_data["Random Price"] = chart_data["Price"].round(2)
    chart_data["Random Volume"] = chart_data["Volume"]

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

    st.line_chart(chart_data.set_index("Date")["Random Price"])
    st.dataframe(chart_data[["Stock", "Random Price", "Random Volume", "Date"]])

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

# Merge updated yearly price and volume back into the daily data to update accordingly
draggable_line = draggable_line.merge(
    updated_yearly_data[["Year", "Random Price", "Random Volume"]],
    on="Year",
    suffixes=("", "_updated")
)

# Replace daily Random Price and Random Volume with yearly updated values
draggable_line["Random Price"] = draggable_line["Random Price_updated"]
draggable_line["Random Volume"] = draggable_line["Random Volume_updated"]
draggable_line = draggable_line.drop(columns=["Random Price_updated", "Random Volume_updated"])

# Show the updated daily data with adjusted prices and volumes
st.dataframe(draggable_line[["Stock", "Random Price", "Random Volume", "Date"]])
