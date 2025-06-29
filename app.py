import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta


# App title
st.set_page_config(page_title="Real-Time Stock Market Dashboard", layout="wide")
st.title("📈 Real-Time Stock Market Dashboard")

# Sidebar - User input
st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, INFY)", "AAPL")

start_date = st.sidebar.date_input("Start Date", datetime.today() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Fetch data
@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data

data = load_data(ticker)

# Show raw data
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader(f"Raw Data for {ticker}")
    st.write(data)

# Plot closing price
st.subheader(f"📊 Closing Price of {ticker}")
fig_close = go.Figure()
fig_close.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close'))
fig_close.update_layout(xaxis_title='Date', yaxis_title='Closing Price (USD)')
st.plotly_chart(fig_close, use_container_width=True)

# Plot volume
st.subheader(f"📉 Trading Volume of {ticker}")
fig_volume = go.Figure()
fig_volume.add_trace(go.Bar(x=data['Date'], y=data['Volume'], name='Volume', marker_color='orange'))
fig_volume.update_layout(xaxis_title='Date', yaxis_title='Volume')
st.plotly_chart(fig_volume, use_container_width=True)

# Key indicators
st.sidebar.markdown("---")
st.sidebar.subheader("📌 Latest Stats")
st.sidebar.write("**Last Close Price:**", round(data['Close'].iloc[-1], 2))
st.sidebar.write("**High:**", round(data['High'].max(), 2))
st.sidebar.write("**Low:**", round(data['Low'].min(), 2))
st.sidebar.write("**Average Volume:**", int(data['Volume'].mean()))

