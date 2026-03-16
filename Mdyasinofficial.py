import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime
import time

st.set_page_config(page_title="Yasin AI Signal", layout="wide")

# পাসওয়ার্ড সুরক্ষা
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Yasin AI Access")
    pin = st.text_input("৬ সংখ্যার পিন দিন:", type="password")
    if st.button("Login"):
        if pin == "654321":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("ভুল পিন!")
    st.stop()

# ড্যাশবোর্ড
st.title("🚀 Yasin Official AI Smart Signal")

markets = {
    "🇵🇰 USD/PKR": "USDPKR=X",
    "🇲🇽 USD/MXN": "USDMXN=X",
    "🇧🇷 USD/BRL": "USDBRL=X",
    "🇳🇿 USD/NZD": "USDNZD=X",
    "🇨🇴 USD/COP": "USDCOP=X",
    "🇦🇷 USD/ARS": "USDARS=X",
    "🇩🇿 USD/DZD": "USDDZD=X"
}

symbol_label = st.sidebar.selectbox("মার্কেট:", list(markets.keys()))
symbol = markets[symbol_label]
tf = st.sidebar.selectbox("টাইমফ্রেম:", ["1m", "5m", "15m", "1h"])

try:
    data = yf.download(symbol, period="2d", interval=tf)
    if not data.empty:
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['EMA'] = ta.ema(data['Close'], length=200)
        last = data.iloc[-1]
        
        # সিগন্যাল লজিক
        signal, color = "⌛ WAIT", "#555555"
        if last['Close'] > last['EMA'] and last['RSI'] < 35:
            signal, color = "🔥 BUY", "#00FF00"
        elif last['Close'] < last['EMA'] and last['RSI'] > 65:
            signal, color = "📉 SELL", "#FF0000"
            
        st.markdown(f"""
            <div style="background-color:{color}22; border:3px solid {color}; padding:30px; border-radius:15px; text-align:center;">
                <h1 style="color:{color}; font-size:60px;">{signal}</h1>
                <h2 style="color:white;">প্রাইস: {data['Close'].iloc[-1]:.4f}</h2>
            </div>
        """, unsafe_allow_html=True)
        st.line_chart(data['Close'])
except:
    st.error("ডাটা পাওয়া যাচ্ছে না।")

time.sleep(60)
st.rerun()
