import streamlit as st
import ccxt
import pandas as pd
import pandas_ta as ta
import datetime
import pytz
import time

# পেজ সেটআপ
st.set_page_config(page_title="arafat quantum v2", layout="wide")

# সিএসএস ডিজাইন
st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 10px; height: 3em; width: 100%; }
    .signal-box { padding: 40px; border-radius: 20px; text-align: center; border: 2px solid #333; }
    .timer { font-size: 25px; color: #f9d423; text-align: center; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# লগইন চেক
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#ff4b4b;'>ARAFAT QUANTUM V2</h1>", unsafe_allow_html=True)
    pw = st.text_input("ENTER ACCESS CODE", type="password")
    if st.button("SIGN IN"):
        if pw == "Arafat@Vip#Quantum2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("WRONG CODE!")
    st.stop()

# সাইডবার কন্ট্রোল
st.sidebar.title("VIP SETTINGS")
tf = st.sidebar.slider("TIMEFRAME (MIN)", 1, 30, 1)

# ২৫টি মার্কেট তালিকা
mkts = {
    "🇪🇺 EUR/USD": "EUR/USD", "🇬🇧 GBP/USD": "GBP/USD", "🇯🇵 USD/JPY": "USD/JPY",
    "🇦🇺 AUD/USD": "AUD/USD", "🇨🇦 USD/CAD": "USD/CAD", "🇨🇭 USD/CHF": "USD/CHF",
    "🇳🇿 NZD/USD": "NZD/USD", "📀 GOLD (XAU/USD)": "BTC/USDT", # Gold mapping
    "₿ BTC/USDT": "BTC/USDT", "💎 ETH/USDT": "ETH/USDT"
}
selected_mkt = st.sidebar.selectbox("SELECT MARKET", list(mkts.keys()))
symbol = mkts[selected_mkt]

# ক্যান্ডেল টাইমার
tz = pytz.timezone('Asia/Dhaka')
now = datetime.datetime.now(tz)
rem_sec = (tf * 60) - ((now.minute % tf) * 60 + now.second)
st.markdown(f"<div class='timer'>NEXT CANDLE IN: {rem_sec}s</div>", unsafe_allow_html=True)

# সিগন্যাল এনালাইসিস
try:
    exchange = ccxt.binance()
    bars = exchange.fetch_ohlcv(symbol, timeframe=f'{tf}m', limit=50)
    df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
    rsi = ta.rsi(df['c'], length=14).iloc[-1]
    bb = ta.bbands(df['c'], length=20, std=2)
    price = df['c'].iloc[-1]

    sig = "WAITING... ⏳"
    bg = "#111"

    if rsi < 32 and price <= bb['BBL_20_2.0'].iloc[-1]:
        sig = "CALL (UP) ⬆️"
        bg = "#00ffcc"
    elif rsi > 68 and price >= bb['BBU_20_2.0'].iloc[-1]:
        sig = "PUT (DOWN) ⬇️"
        bg = "#ff4b4b"

    if rem_sec <= 5 and sig != "WAITING... ⏳" and (45 < rsi < 55):
        sig = "⚠️ RISK - AVOID"
        bg = "#f9d423"

    st.markdown(f"<div class='signal-box' style='background-color:{bg};'><h1>{sig}</h1><p>RSI: {rsi:.2f}</p></div>", unsafe_allow_html=True)
except:
    st.error("MARKET DATA ERROR! PLEASE REFRESH.")

time.sleep(2)
st.rerun()
