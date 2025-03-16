import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
import yfinance as yf
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#initializing vader model to analyze +/- news
sia = SentimentIntensityAnalyzer()

#fetch stock data from Yahoo Finance
def get_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df.reset_index(inplace=True)#date a column not index
    df.rename(columns={df.columns[0]: "Date"}, inplace=True)
    df.columns = df.columns.map(lambda x: x[0] if isinstance(x, tuple) else x)#to handle multi-index columns in case of tuple return values
    return df

#preprocess data: add averages for daily and monthly
def preprocess_data(df):
    if df.empty:
        return df
    #adds a new colum with Avg which calculates 1/5/22/50/200 days prev rows of close
    df['Daily Avg'] = df['Close'].rolling(window=1).mean()
    df['Weekly Avg'] = df['Close'].rolling(window=5).mean()
    df['Monthly Avg'] = df['Close'].rolling(window=22).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    return df

# Fetch Stock News & Perform Sentiment Analysis
def fetch_stock_news(ticker):
    api_key = "5739c1e37b624deaa1024adad4067c1e"#your own api key
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()["articles"][:5]#get 5 recent articles
        sentiments = []#to store the sentiment scores
        for article in articles:
            sentiment_score = sia.polarity_scores(article["title"])['compound']
            sentiments.append(sentiment_score)#it is a function that calculates sentiment scores for a text from nltk
        avg_sentiment = np.mean(sentiments) if sentiments else 0
        return avg_sentiment, articles
    return 0, []

# Calculate Profit/Loss in INR
def calculate_profit_loss(df, investment_amount, purchase_date):
    df['Date'] = pd.to_datetime(df['Date'])
    purchase_data = df[df['Date'] == pd.to_datetime(purchase_date)]
    if purchase_data.empty:
        return None, None
    purchase_price = purchase_data['Close'].values[0]
    latest_price = df['Close'].iloc[-1]#stock's recent closing price
    shares_bought = investment_amount / purchase_price
    final_value = shares_bought * latest_price
    profit_loss = final_value - investment_amount
    return profit_loss, final_value

# Streamlit App
def app():
    st.title("Stock Price Prediction & Analysis")
    ticker = st.selectbox("Select Stock", ["AAPL", "GOOG", "MSFT", "AMZN"])
    start_date = st.date_input("Start Date", pd.to_datetime('2021-01-01'))
    end_date = st.date_input("End Date", pd.to_datetime('2023-01-01'))
    df = get_stock_data(ticker, start_date, end_date)#gets from yf
    
    if df.empty:
        st.error("No data available for the selected period. Please try another date range.")
        return
    
    st.subheader("Stock Price Data")
    st.write(df)#entire table
    df = preprocess_data(df)
    st.subheader("Preprocessed Data")
    st.write(df[['Date', 'Close', 'Daily Avg', 'Weekly Avg', 'Monthly Avg', 'SMA_50', 'SMA_200']].tail())#only last few rows
    df['Date'] = df['Date'].astype(str)#for plotly use
    fig = px.line(df, x='Date', y=['Close', 'SMA_50', 'SMA_200'], title="Stock Price with SMA")
    st.plotly_chart(fig)
    
    # Stock Sentiment Analysis
    st.subheader("Stock News Sentiment Analysis")
    sentiment_score, news_articles = fetch_stock_news(ticker)
    if news_articles:
        for article in news_articles:
            st.write(f"- {article['title']}")
    st.write("Sentiment Score:", sentiment_score)
    
    st.subheader("Trading Signals")
    latest_price = df['Close'].iloc[-1]
    if latest_price > df['SMA_50'].iloc[-1]:
        st.write("Uptrend - Possible BUY signal")
    elif latest_price < df['SMA_200'].iloc[-1]:
        st.write("Downtrend - Possible SELL signal")
    else:
        st.write("Neutral - HOLD signal")
    
    # Profit/Loss Calculator
    st.subheader("Profit/Loss Calculator")
    investment_amount = st.number_input("Investment Amount (₹)", min_value=1000, step=1000)
    purchase_date = st.date_input("Purchase Date", min_value=start_date, max_value=end_date)
    if st.button("Calculate Profit/Loss"):
        profit_loss, final_value = calculate_profit_loss(df, investment_amount, purchase_date)
        if profit_loss is not None:
            st.write(f"Final Portfolio Value: ₹{final_value:.2f}")
            if profit_loss > 0:
                st.success(f"Profit: ₹{profit_loss:.2f}")
            else:
                st.error(f"Loss: ₹{profit_loss:.2f}")
        else:
            st.warning("No data available for the selected purchase date.")

if __name__ == "__main__":
    app()