import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

from draggable_charts import line_chart

st.title("Global Stock Market Price History")

df = yf.download([
    "MMM", "AOS", "ABT", "ABBV", "ACN", "ATVI", "AYI", "ADBE", "AAP", "AMD",
    "AES", "AFL", "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALGN", "ALLE",
    "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AMCR", "AEE", "AAL", "AEP",
    "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "ADI",
    "ANSS", "AON", "APA", "AAPL", "AMAT", "APTV", "ACGL", "ADM", "ANET", "AJG",
    "AIZ", "T", "ATO", "ADSK", "ADP", "AZO", "AVB", "AVY", "AXON", "BKR",
    "BALL", "BAC", "BBWI", "BAX", "BDX", "BRK.B", "BBY", "BIO", "TECH", "BIIB",
    "BLK", "BK", "BA", "BKNG", "BWA", "BXP", "BSX", "BMY", "AVGO", "BR",
    "BRO", "BF.B", "BG", "CHRW", "CDNS", "CZR", "CPB", "COF", "CAH", "KMX",
    "CCL", "CARR", "CTLT", "CAT", "CBOE", "CBRE", "CDW", "CE", "CNC", "CNP",
    "CDAY", "CF", "CRL", "SCHW", "CHTR", "CVX", "CMG", "CB", "CHD", "CI",
    "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS", "CLX", "CME", "CMS", "KO",
    "CTSH", "CL", "CMCSA", "CMA", "CAG", "COP", "ED", "STZ", "CEG", "COO",
    "CPRT", "GLW", "CTVA", "CSGP", "COST", "CTRA", "CCI", "CSX", "CMI", "CVS",
    "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "XRAY", "DVN", "DXCM", "FANG",
    "DLR", "DFS", "DIS", "DG", "DLTR", "D", "DOV", "DOW", "DTE", "DUK",
    "DD", "DXC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "ELV",
    "LLY", "EMR", "ENPH", "ETR", "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR",
    "ESS", "EL", "ETSY", "EVRG", "ES", "RE", "EXC", "EXPE", "EXPD", "EXR",
    "XOM", "FFIV", "FDS", "FAST", "FRT", "FDX", "FITB", "FSLR", "FE", "FIS",
    "FISV", "FLT", "FMC", "F", "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX",
    "GRMN", "IT", "GEHC", "GEN", "GNRC", "GD", "GE", "GIS", "GM", "GPC",
    "GILD", "GL", "GPN", "GS", "HAL", "HIG", "HAS", "HCA", "PEAK", "HSIC",
    "HSY", "HES", "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM",
    "HPQ", "HUM", "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW", "ILMN", "INCY",
    "IR", "INTC", "ICE", "IP", "IPG", "INTU", "ISRG", "IVZ", "INVH", "IQV",
    "IRM", "JBHT", "JKHY", "J", "JNJ", "JCI", "JPM", "JNPR", "K", "KDP",
    "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX", "LH",
    "LRCX", "LW", "LVS", "LDOS", "LEN", "LIN", "LYV", "LKQ", "LMT", "L",
    "LOW", "LUMN", "LYB", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM",
    "MAS", "MA", "MTCH", "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET",
    "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", "TAP",
    "MDLZ", "MPWR", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "NDAQ", "NTAP",
    "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NKE", "NI", "NDSN", "NSC",
    "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY",
    "ODFL", "OMC", "ON", "OKE", "ORCL", "OGN", "OTIS", "PCAR", "PKG", "PANW",
    "PARA", "PH", "PAYX", "PAYC", "PYPL", "PNR", "PBCT", "PEP", "PKI", "PFE",
    "PCG", "PM", "PSX", "PNW", "PXD", "PNC", "POOL", "PPG", "PPL", "PFG",
    "PG", "PGR", "PLD", "PRU", "PEG", "PTC", "PSA", "PHM", "QRVO", "PWR",
    "QCOM", "DGX", "RL", "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG",
    "RMD", "RHI", "ROK", "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC",
    "SLB", "STX", "SEE", "SRE", "NOW", "SHW", "SPG", "SWKS", "SJM", "SNA",
    "SEDG", "SO", "LUV", "SWK", "SBUX", "STT", "STE", "SYK", "SIVB", "SYF",
    "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL", "TDY",
    "TFX", "TER", "TSLA", "TXN", "TXT", "TMO", "TJX", "TSCO", "TT", "TDG",
    "TRV", "TRMB", "TFC", "TYL", "TSN", "USB", "UDR", "ULTA", "UNP", "UAL",
    "UPS", "URI", "UNH", "UHS", "VLO", "VTR", "VRSN", "VRSK", "VZ", "VRTX",
    "VFC", "VTRS", "VICI", "V", "VMC", "WAB", "WBA", "WMT", "WBD", "WM",
    "WAT", "WEC", "WFC", "WELL", "WST", "WDC", "WRK", "WY", "WHR", "WMB",
    "WTW", "WYNN", "XEL", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"
], start="2020-01-01", end="2025-01-01")
df = df.reset_index()

choose_stock = st.selectbox("Choose a stock:", [
    "MMM", "AOS", "ABT", "ABBV", "ACN", "ATVI", "AYI", "ADBE", "AAP", "AMD",
    "AES", "AFL", "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALGN", "ALLE",
    "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AMCR", "AEE", "AAL", "AEP",
    "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "ADI",
    "ANSS", "AON", "APA", "AAPL", "AMAT", "APTV", "ACGL", "ADM", "ANET", "AJG",
    "AIZ", "T", "ATO", "ADSK", "ADP", "AZO", "AVB", "AVY", "AXON", "BKR",
    "BALL", "BAC", "BBWI", "BAX", "BDX", "BRK.B", "BBY", "BIO", "TECH", "BIIB",
    "BLK", "BK", "BA", "BKNG", "BWA", "BXP", "BSX", "BMY", "AVGO", "BR",
    "BRO", "BF.B", "BG", "CHRW", "CDNS", "CZR", "CPB", "COF", "CAH", "KMX",
    "CCL", "CARR", "CTLT", "CAT", "CBOE", "CBRE", "CDW", "CE", "CNC", "CNP",
    "CDAY", "CF", "CRL", "SCHW", "CHTR", "CVX", "CMG", "CB", "CHD", "CI",
    "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS", "CLX", "CME", "CMS", "KO",
    "CTSH", "CL", "CMCSA", "CMA", "CAG", "COP", "ED", "STZ", "CEG", "COO",
    "CPRT", "GLW", "CTVA", "CSGP", "COST", "CTRA", "CCI", "CSX", "CMI", "CVS",
    "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "XRAY", "DVN", "DXCM", "FANG",
    "DLR", "DFS", "DIS", "DG", "DLTR", "D", "DOV", "DOW", "DTE", "DUK",
    "DD", "DXC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "ELV",
    "LLY", "EMR", "ENPH", "ETR", "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR",
    "ESS", "EL", "ETSY", "EVRG", "ES", "RE", "EXC", "EXPE", "EXPD", "EXR",
    "XOM", "FFIV", "FDS", "FAST", "FRT", "FDX", "FITB", "FSLR", "FE", "FIS",
    "FISV", "FLT", "FMC", "F", "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX",
    "GRMN", "IT", "GEHC", "GEN", "GNRC", "GD", "GE", "GIS", "GM", "GPC",
    "GILD", "GL", "GPN", "GS", "HAL", "HIG", "HAS", "HCA", "PEAK", "HSIC",
    "HSY", "HES", "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM",
    "HPQ", "HUM", "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW", "ILMN", "INCY",
    "IR", "INTC", "ICE", "IP", "IPG", "INTU", "ISRG", "IVZ", "INVH", "IQV",
    "IRM", "JBHT", "JKHY", "J", "JNJ", "JCI", "JPM", "JNPR", "K", "KDP",
    "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX", "LH",
    "LRCX", "LW", "LVS", "LDOS", "LEN", "LIN", "LYV", "LKQ", "LMT", "L",
    "LOW", "LUMN", "LYB", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM",
    "MAS", "MA", "MTCH", "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET",
    "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", "TAP",
    "MDLZ", "MPWR", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "NDAQ", "NTAP",
    "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NKE", "NI", "NDSN", "NSC",
    "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY",
    "ODFL", "OMC", "ON", "OKE", "ORCL", "OGN", "OTIS", "PCAR", "PKG", "PANW",
    "PARA", "PH", "PAYX", "PAYC", "PYPL", "PNR", "PBCT", "PEP", "PKI", "PFE",
    "PCG", "PM", "PSX", "PNW", "PXD", "PNC", "POOL", "PPG", "PPL", "PFG",
    "PG", "PGR", "PLD", "PRU", "PEG", "PTC", "PSA", "PHM", "QRVO", "PWR",
    "QCOM", "DGX", "RL", "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG",
    "RMD", "RHI", "ROK", "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC",
    "SLB", "STX", "SEE", "SRE", "NOW", "SHW", "SPG", "SWKS", "SJM", "SNA",
    "SEDG", "SO", "LUV", "SWK", "SBUX", "STT", "STE", "SYK", "SIVB", "SYF",
    "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL", "TDY",
    "TFX", "TER", "TSLA", "TXN", "TXT", "TMO", "TJX", "TSCO", "TT", "TDG",
    "TRV", "TRMB", "TFC", "TYL", "TSN", "USB", "UDR", "ULTA", "UNP", "UAL",
    "UPS", "URI", "UNH", "UHS", "VLO", "VTR", "VRSN", "VRSK", "VZ", "VRTX",
    "VFC", "VTRS", "VICI", "V", "VMC", "WAB", "WBA", "WMT", "WBD", "WM",
    "WAT", "WEC", "WFC", "WELL", "WST", "WDC", "WRK", "WY", "WHR", "WMB",
    "WTW", "WYNN", "XEL", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"
])

ticker_info = yf.Ticker(choose_stock).info
long_name = ticker_info.get("longName", choose_stock)

if choose_stock:
    chart_data = pd.DataFrame({
        "type": ["Stock"] * len(df),
        "challenge_id": st.number_input("Input a challenge_id", value=0),
        "Name": [choose_stock] * len(df),
        "long_name": [long_name] * len(df),
        "Price": df["Close"][choose_stock].round(2),
        "Volume": df["Volume"][choose_stock],
        "Date": df["Date"].dt.date
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
