import streamlit as st
import ccxt
import pandas as pd
import pandas_ta as ta

# পেজ টাইটেল
st.title("🚀 Yasin AI Forex Prediction")

# ইনপুট এবং মানি ম্যানেজমেন্ট
if 'bet' not in st.session_state:
    st.session_state.bet = 1.0

# কারেন্সি পেয়ার
symbol = st.selectbox("সিলেক্ট মার্কেট", ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD'])

def fetch_signal(symbol):
    try:
        ex = ccxt.binance()
        bars = ex.fetch_ohlcv(symbol, timeframe='1m', limit=50)
        df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
        df['rsi'] = ta.rsi(df['c'], length=14)
        
        last_rsi = df['rsi'].iloc[-1]
        price = df['c'].iloc[-1]
        
        if last_rsi < 30:
            return f"🟢 BUY (Next Candle UP) | Price: {price}", "green"
        elif last_rsi > 70:
            return f"🔴 SELL (Next Candle DOWN) | Price: {price}", "red"
        else:
            return f"⏳ Waiting... | Price: {price}", "gray"
    except:
        return "⚠️ Connection Error", "black"

# সিগন্যাল ডিসপ্লে
sig_text, sig_color = fetch_signal(symbol)
st.subheader(f"সিগন্যাল: :{sig_color}[{sig_text}]")

st.divider()

# মানি ম্যানেজমেন্ট সেকশন
st.write(f"💵 বর্তমান ট্রেড অ্যামাউন্ট: **${st.session_state.bet:.2f}**")
col1, col2 = st.columns(2)

if col1.button("✅ WIN (Reset to $1)"):
    st.session_state.bet = 1.0
    st.rerun()

if col2.button("❌ LOSS (Martingale)"):
    st.session_state.bet *= 2.2
    st.rerun()
