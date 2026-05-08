import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


st.set_page_config(page_title="Stock Analysis System", layout="wide")
st.title("📈 Stock Market Analysis System")
st.markdown("### Secure Entrepreneurial & Legal Assistance (SELA) Project")

st.sidebar.header("Search Parameters")
ticker_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, MSFT)", value="AAPL").upper()
time_period = st.sidebar.selectbox("Select Time Period", ["7 Days", "1 Month", "1 Year"])


period_map = {"7 Days": "7d", "1 Month": "1mo", "1 Year": "1y"}

if ticker_symbol:
    try:
        
        stock_data = yf.Ticker(ticker_symbol)

        info = stock_data.info
        company_name = info.get('longName', 'N/A')
        current_price = info.get('currentPrice', 'N/A')
        currency = info.get('currency', 'USD')

        hist = stock_data.history(period=period_map[time_period])

        if hist.empty:
            st.error(f"No data found for symbol: {ticker_symbol}")
        else:
           
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label=f"Current Price ({company_name})", value=f"{current_price} {currency}")
            
            with col2:
                daily_change = hist['Close'].iloc[-1] - hist['Close'].iloc[0]
                st.metric(label="Period Change", value=f"{daily_change:.2f}", delta=f"{daily_change:.2f}")

           
            display_df = hist[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10)
            
          
            st.subheader(f"{ticker_symbol} Price Trend - {time_period}")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(hist.index, hist['Close'], color='#0078D4', linewidth=2)
            ax.set_ylabel("Price")
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.xticks(rotation=45)
            st.pyplot(fig)

            st.subheader("Recent Historical Data")
            st.dataframe(display_df, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}. Please check the stock symbol and try again.")
else:
    st.info("Please enter a stock symbol in the sidebar to begin.")


st.sidebar.markdown("---")
st.sidebar.write("**Project Team:**")
st.sidebar.write("1. [Iman Ali] - Lead/Backend")
st.sidebar.write("2. [Mariam Sahdy] - UI/Viz")
