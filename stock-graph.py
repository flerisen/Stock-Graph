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

long_names = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "AMZN": "Amazon.com, Inc.",
    "NVDA": "NVIDIA Corporation",
    "GOOGL": "Alphabet Inc. Class A",
    "GOOG": "Alphabet Inc. Class C",
    "META": "Meta Platforms, Inc.",
    "BRK.B": "Berkshire Hathaway Inc. Class B",
    "TSLA": "Tesla, Inc.",
    "UNH": "UnitedHealth Group Incorporated",
    "LLY": "Eli Lilly and Company",
    "JPM": "JPMorgan Chase & Co.",
    "XOM": "Exxon Mobil Corporation",
    "JNJ": "Johnson & Johnson",
    "V": "Visa Inc.",
    "PG": "Procter & Gamble Company",
    "AVGO": "Broadcom Inc.",
    "MA": "Mastercard Incorporated",
    "HD": "The Home Depot, Inc.",
    "CVX": "Chevron Corporation",
    "KO": "The Coca-Cola Company",
    "PEP": "PepsiCo, Inc.",
    "WMT": "Walmart Inc.",
    "BAC": "Bank of America Corporation",
    "CSCO": "Cisco Systems, Inc.",
    "ADBE": "Adobe Inc.",
    "CMCSA": "Comcast Corporation",
    "NFLX": "Netflix, Inc.",
    "ABT": "Abbott Laboratories",
    "CRM": "Salesforce, Inc.",
    "ORCL": "Oracle Corporation",
    "MRK": "Merck & Co., Inc.",
    "TMO": "Thermo Fisher Scientific Inc.",
    "INTC": "Intel Corporation",
    "ACN": "Accenture plc",
    "COST": "Costco Wholesale Corporation",
    "MCD": "McDonald's Corporation",
    "DHR": "Danaher Corporation",
    "AMD": "Advanced Micro Devices, Inc.",
    "NEE": "NextEra Energy, Inc.",
    "DIS": "The Walt Disney Company",
    "IBM": "International Business Machines Corporation",
    "TXN": "Texas Instruments Incorporated",
    "LIN": "Linde plc",
    "PM": "Philip Morris International Inc.",
    "NKE": "NIKE, Inc.",
    "QCOM": "QUALCOMM Incorporated",
    "AMGN": "Amgen Inc.",
    "HON": "Honeywell International Inc.",
    "UNP": "Union Pacific Corporation",
    "MDT": "Medtronic plc",
    "GE": "General Electric Company",
    "UPS": "United Parcel Service, Inc.",
    "LOW": "Lowe's Companies, Inc.",
    "SBUX": "Starbucks Corporation",
    "CAT": "Caterpillar Inc.",
    "GS": "The Goldman Sachs Group, Inc.",
    "INTU": "Intuit Inc.",
    "BLK": "BlackRock, Inc.",
    "ISRG": "Intuitive Surgical, Inc.",
    "CVS": "CVS Health Corporation",
    "MS": "Morgan Stanley",
    "AMAT": "Applied Materials, Inc.",
    "CI": "Cigna Corporation",
    "VRTX": "Vertex Pharmaceuticals Incorporated",
    "BA": "The Boeing Company",
    "DE": "Deere & Company",
    "NOW": "ServiceNow, Inc.",
    "LMT": "Lockheed Martin Corporation",
    "ADI": "Analog Devices, Inc.",
    "T": "AT&T Inc.",
    "SYK": "Stryker Corporation",
    "ZTS": "Zoetis Inc.",
    "PFE": "Pfizer Inc.",
    "SPGI": "S&P Global Inc.",
    "MO": "Altria Group, Inc.",
    "PLD": "Prologis, Inc.",
    "ELV": "Elevance Health, Inc.",
    "EL": "The Estée Lauder Companies Inc.",
    "BDX": "Becton, Dickinson and Company",
    "BKNG": "Booking Holdings Inc.",
    "MMC": "Marsh & McLennan Companies, Inc.",
    "SO": "The Southern Company",
    "GILD": "Gilead Sciences, Inc.",
    "AXP": "American Express Company",
    "ADP": "Automatic Data Processing, Inc.",
    "C": "Citigroup Inc.",
    "TJX": "The TJX Companies, Inc.",
    "REGN": "Regeneron Pharmaceuticals, Inc.",
    "CL": "Colgate-Palmolive Company",
    "DUK": "Duke Energy Corporation",
    "BSX": "Boston Scientific Corporation",
    "FDX": "FedEx Corporation",
    "APD": "Air Products and Chemicals, Inc.",
    "ETN": "Eaton Corporation plc",
    "PNC": "The PNC Financial Services Group, Inc.",
    "EOG": "EOG Resources, Inc.",
    "GM": "General Motors Company",
    "ITW": "Illinois Tool Works Inc.",
    "CB": "Chubb Limited",
    "USB": "U.S. Bancorp",
    "FIS": "Fidelity National Information Services, Inc.",
    "WM": "Waste Management, Inc.",
    "SCHW": "The Charles Schwab Corporation",
    "NSC": "Norfolk Southern Corporation",
    "EW": "Edwards Lifesciences Corporation",
    "TGT": "Target Corporation",
    "AON": "Aon plc",
    "MDLZ": "Mondelez International, Inc.",
    "HUM": "Humana Inc.",
    "PGR": "The Progressive Corporation",
    "FISV": "Fiserv, Inc.",
    "CME": "CME Group Inc.",
    "TRV": "The Travelers Companies, Inc.",
    "MET": "MetLife, Inc.",
    "AEP": "American Electric Power Company, Inc.",
    "PSA": "Public Storage",
    "SHW": "The Sherwin-Williams Company",
    "ICE": "Intercontinental Exchange, Inc.",
    "MCO": "Moody's Corporation",
    "D": "Dominion Energy, Inc.",
    "EMR": "Emerson Electric Co.",
    "ROST": "Ross Stores, Inc.",
    "ECL": "Ecolab Inc.",
    "AIG": "American International Group, Inc.",
    "MAR": "Marriott International, Inc.",
    "MPC": "Marathon Petroleum Corporation",
    "ALL": "The Allstate Corporation",
    "ORLY": "O'Reilly Automotive, Inc.",
    "KMB": "Kimberly-Clark Corporation",
    "STZ": "Constellation Brands, Inc.",
    "SRE": "Sempra Energy",
    "WELL": "Welltower Inc.",
    "HCA": "HCA Healthcare, Inc.",
    "CTAS": "Cintas Corporation",
    "LRCX": "Lam Research Corporation",
    "IDXX": "IDEXX Laboratories, Inc.",
    "NOC": "Northrop Grumman Corporation",
    "WMB": "The Williams Companies, Inc.",
    "CMG": "Chipotle Mexican Grill, Inc.",
    "ADSK": "Autodesk, Inc.",
    "NEM": "Newmont Corporation",
    "DLR": "Digital Realty Trust, Inc.",
    "O": "Realty Income Corporation",
    "AFL": "Aflac Incorporated",
    "TEL": "TE Connectivity Ltd.",
    "CDNS": "Cadence Design Systems, Inc.",
    "PCAR": "PACCAR Inc.",
    "SPG": "Simon Property Group, Inc.",
    "PH": "Parker-Hannifin Corporation",
    "VLO": "Valero Energy Corporation",
    "FTNT": "Fortinet, Inc.",
    "PSX": "Phillips 66",
    "MNST": "Monster Beverage Corporation",
    "CTSH": "Cognizant Technology Solutions Corporation",
    "KLAC": "KLA Corporation",
    "ROP": "Roper Technologies, Inc.",
    "KHC": "The Kraft Heinz Company",
    "EXC": "Exelon Corporation",
    "PAYX": "Paychex, Inc.",
    "HPQ": "HP Inc.",
    "MSI": "Motorola Solutions, Inc.",
    "BAX": "Baxter International Inc.",
    "WEC": "WEC Energy Group, Inc.",
    "AZO": "AutoZone, Inc.",
    "HES": "Hess Corporation",
    "PRU": "Prudential Financial, Inc.",
    "MCK": "McKesson Corporation",
    "VRSK": "Verisk Analytics, Inc.",
    "DOW": "Dow Inc.",
    "PEG": "Public Service Enterprise Group Incorporated",
    "SYY": "Sysco Corporation",
    "DG": "Dollar General Corporation",
    "WBA": "Walgreens Boots Alliance, Inc.",
    "CMI": "Cummins Inc.",
    "MTD": "Mettler-Toledo International Inc.",
    "TT": "Trane Technologies plc",
    "CHD": "Church & Dwight Co., Inc.",
    "XYL": "Xylem Inc.",
    "ZBH": "Zimmer Biomet Holdings, Inc.",
    "ED": "Consolidated Edison, Inc.",
    "NUE": "Nucor Corporation",
    "CNC": "Centene Corporation",
    "KEYS": "Keysight Technologies Incorporated",
    "WST": "West Pharmaceutical Services, Inc.",
    "AMP": "Ameriprise Financial, Inc.",
    "HAL": "Halliburton Company",
    "ANET": "Arista Networks, Inc.",
    "AVB": "AvalonBay Communities, Inc.",
    "FTV": "Fortive Corporation",
    "F": "Ford Motor Company",
    "PPG": "PPG Industries, Inc.",
    "STT": "State Street Corporation",
    "RSG": "Republic Services, Inc.",
    "DLTR": "Dollar Tree, Inc.",
    "MLM": "Martin Marietta Materials, Inc.",
    "TSCO": "Tractor Supply Company",
    "LEN": "Lennar Corporation",
    "EIX": "Edison International",
    "CARR": "Carrier Global Corporation",
    "FAST": "Fastenal Company",
    "GWW": "W.W. Grainger, Inc.",
    "VFC": "VF Corporation",
    "IFF": "International Flavors & Fragrances Inc.",
    "BKR": "Baker Hughes Company",
    "A": "Agilent Technologies, Inc.",
    "HIG": "The Hartford Financial Services Group, Inc.",
    "CTVA": "Corteva, Inc.",
    "DHI": "D.R. Horton, Inc.",
    "HOLX": "Hologic, Inc.",
    "AKAM": "Akamai Technologies, Inc.",
    "ALB": "Albemarle Corporation",
    "PPL": "PPL Corporation",
    "DTE": "DTE Energy Company",
    "ETR": "Entergy Corporation",
    "LUV": "Southwest Airlines Co.",
    "VTR": "Ventas, Inc.",
    "EXR": "Extra Space Storage Inc.",
    "CNP": "CenterPoint Energy, Inc.",
    "NTRS": "Northern Trust Corporation",
    "ES": "Eversource Energy",
    "NTAP": "NetApp, Inc.",
    "CMS": "CMS Energy Corporation",
    "HPE": "Hewlett Packard Enterprise Company",
    "FMC": "FMC Corporation",
    "DRI": "Darden Restaurants, Inc.",
    "EFX": "Equifax Inc.",
    "AEE": "Ameren Corporation",
    "WAT": "Waters Corporation",
    "NDAQ": "Nasdaq, Inc.",
    "ZBRA": "Zebra Technologies Corporation",
    "ATO": "Atmos Energy Corporation",
    "SWK": "Stanley Black & Decker, Inc.",
    "EQR": "Equity Residential",
    "MTB": "M&T Bank Corporation",
    "GLW": "Corning Incorporated",
    "NVR": "NVR, Inc.",
    "HBAN": "Huntington Bancshares Incorporated",
    "RMD": "ResMed Inc.",
    "PWR": "Quanta Services, Inc.",
    "TSN": "Tyson Foods, Inc.",
    "VMC": "Vulcan Materials Company",
    "KMI": "Kinder Morgan, Inc.",
    "GRMN": "Garmin Ltd.",
    "LHX": "L3Harris Technologies, Inc.",
    "STX": "Seagate Technology Holdings plc",
    "DOV": "Dover Corporation",
    "SJM": "The J. M. Smucker Company",
    "MKC": "McCormick & Company, Incorporated",
    "ARE": "Alexandria Real Estate Equities, Inc.",
    "ALGN": "Align Technology, Inc.",
    "CHRW": "C.H. Robinson Worldwide, Inc.",
    "KDP": "Keurig Dr Pepper Inc.",
    "GPC": "Genuine Parts Company",
    "BXP": "Boston Properties, Inc.",
    "NDSN": "Nordson Corporation",
    "JKHY": "Jack Henry & Associates, Inc.",
    "ESS": "Essex Property Trust, Inc.",
    "UDR": "UDR, Inc.",
    "PKI": "PerkinElmer, Inc.",
    "INCY": "Incyte Corporation",
    "CINF": "Cincinnati Financial Corporation",
    "COO": "The Cooper Companies, Inc.",
    "BHF": "Brighthouse Financial, Inc.",
    "FRC": "First Republic Bank",
    "PKG": "Packaging Corporation of America",
    "MAS": "Masco Corporation",
    "AIZ": "Assurant, Inc.",
    "CF": "CF Industries Holdings, Inc.",
    "HII": "Huntington Ingalls Industries, Inc.",
    "L": "Loews Corporation",
    "WRB": "W. R. Berkley Corporation",
    "NRG": "NRG Energy, Inc.",
    "BBY": "Best Buy Co., Inc.",
    "AVY": "Avery Dennison Corporation",
    "CE": "Celanese Corporation",
    "TYL": "Tyler Technologies, Inc.",
    "EXPD": "Expeditors International of Washington, Inc.",
    "IP": "International Paper Company",
    "HWM": "Howmet Aerospace Inc.",
    "ROL": "Rollins, Inc.",
    "OMC": "Omnicom Group Inc.",
    "NWL": "Newell Brands Inc.",
    "LKQ": "LKQ Corporation",
    "WHR": "Whirlpool Corporation",
    "XRAY": "DENTSPLY SIRONA Inc.",
    "MOS": "The Mosaic Company",
    "APA": "APA Corporation",
    "UHS": "Universal Health Services, Inc.",
    "CAG": "Conagra Brands, Inc.",
    "EMN": "Eastman Chemical Company",
    "DVA": "DaVita Inc.",
    "AAL": "American Airlines Group Inc.",
    "TPR": "Tapestry, Inc.",
    "NCLH": "Norwegian Cruise Line Holdings Ltd.",
    "ALLE": "Allegion plc",
    "FRT": "Federal Realty Investment Trust",
    "HAS": "Hasbro, Inc.",
    "SEE": "Sealed Air Corporation",
    "BEN": "Franklin Resources, Inc.",
    "IVZ": "Invesco Ltd.",
    "RL": "Ralph Lauren Corporation",
    "DXC": "DXC Technology Company",
    "NLSN": "Nielsen Holdings plc",
    "FLIR": "Teledyne Technologies Incorporated",
    "HRB": "H&R Block, Inc.",
    "TAP": "Molson Coors Beverage Company",
    "NWSA": "News Corporation Class A",
    "NWS": "News Corporation Class B",
    "PVH": "PVH Corp.",
    "LB": "L Brands, Inc.",
    "FOX": "Fox Corporation Class B",
    "FOXA": "Fox Corporation Class A",
    "HBI": "Hanesbrands Inc.",
    "MHK": "Mohawk Industries, Inc.",
    "LEG": "Leggett & Platt, Incorporated",
    "DISCA": "Discovery, Inc. Class A",
    "DISCK": "Discovery, Inc. Class C",
    "KSS": "Kohl's Corporation",
    "GPS": "The Gap, Inc.",
    "JWN": "Nordstrom, Inc.",
    "UA": "Under Armour, Inc. Class C",
    "UAA": "Under Armour, Inc. Class A",
    "ADS": "Alliance Data Systems Corporation",
    "CPB": "Campbell Soup Company",
    "NBL": "Noble Energy, Inc.",
    "HFC": "HollyFrontier Corporation",
    "NOV": "NOV Inc.",
    "CXO": "Concho Resources Inc.",
    "DVN": "Devon Energy Corporation",
    "MRO": "Marathon Oil Corporation",
    "OKE": "ONEOK, Inc.",
    "XEC": "Cimarex Energy Co.",
    "COG": "Cabot Oil & Gas Corporation",
    "FANG": "Diamondback Energy, Inc.",
    "PXD": "Pioneer Natural Resources Company",
    "EQT": "EQT Corporation",
    "SWN": "Southwestern Energy Company",
    "RRC": "Range Resources Corporation",
    "AR": "Antero Resources Corporation",
    "CNX": "CNX Resources Corporation",
    "SM": "SM Energy Company",
    "CPE": "Callon Petroleum Company",
    "MTDR": "Matador Resources Company",
    "CRK": "Comstock Resources, Inc.",
    "PDCE": "PDC Energy, Inc.",
    "LPI": "Laredo Petroleum, Inc.",
    "OXY": "Occidental Petroleum Corporation",
    "CLR": "Continental Resources, Inc.",
    "WLL": "Whiting Petroleum Corporation"
}

choose_stock = st.selectbox("Choose a stock:", tickers)

df = yf.download(choose_stock, start="2020-01-01", end="2025-01-01")
df = df.reset_index()

if choose_stock:
    chart_data = pd.DataFrame({
        "type": ["Stock"] * len(df),
        "challenge_id": st.number_input("Input a challenge_id", value=0),
        "long_name": [long_names.get(choose_stock, choose_stock)] * len(df),
        "Name": [choose_stock] * len(df),
        "Price": df["Close"][choose_stock].round(2),
        "Volume": df["Volume"][choose_stock],
        "Date": df["Date"].dt.date
    })
    
    st.subheader("Global Stock Graph 1-1")

    st.line_chart(chart_data.set_index("Date")["Price"])
    st.dataframe(chart_data[["type", "challenge_id","Name", "Price", "Volume", "Date"]])

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
st.dataframe(draggable_line[["type", "challenge_id","Name", "Random Price", "Random Volume", "Date"]])
