
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# Fetch historical data for a stock (e.g., AAPL)
ticker = "AAPL"
df = yf.download(ticker, start="2020-01-01", end="2024-01-01")

# Keep only the 'Close' price for prediction
df = df[['Close']]

# Plot the closing price
plt.figure(figsize=(10,5))
plt.plot(df, label=f'{ticker} Closing Price')
plt.legend()
plt.show()
