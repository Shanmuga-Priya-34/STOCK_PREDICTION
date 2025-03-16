STOCK PRICE PREDICTION 

Stock Price Prediction & Analysis

Overview

This project is a Stock Price Prediction & Analysis tool built using Streamlit. It allows users to fetch stock data, analyze trends, calculate profit/loss, and perform sentiment analysis based on recent stock news.

Features:

•	Fetches historical stock data from Yahoo Finance.

•	Calculates moving averages (Daily, Weekly, Monthly, SMA 50, SMA 200).

•	Displays stock price trends using interactive charts.

•	Analyzes stock sentiment using VADER Sentiment Analysis.

•	Provides trading signals based on stock trends.

•	Includes a Profit/Loss Calculator to evaluate investments in Indian Rupees (₹).

Requirements:

Ensure you have the following Python libraries installed:

              pip install streamlit yfinance plotly nltk requests pandas numpy

How to Run:

1.	Clone this repository or download the script.

2.	Open a terminal and navigate to the project folder.

3.	Run the following command: 

4.	streamlit run stock_prediction.py

5.	Open the provided localhost URL in your browser.

API Keys:

This project uses NewsAPI for fetching stock-related news articles. Replace your own API key in stock_prediction.py with a valid API key from NewsAPI.

Usage:

1.	Select a Stock from the dropdown.

2.	Choose a Date Range for analysis.

3.	View Stock Data and Moving Averages.

4.	Analyze Stock Sentiment based on recent news.

5.	Check Trading Signals (Buy, Sell, Hold).

6.	Use the Profit/Loss Calculator to estimate investment returns.
