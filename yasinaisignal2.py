import streamlit as st
import ccxt
import pandas as pd
import pandas_ta as ta
import datetime
import pytz
import time

# ১. পেজ কনফিগারেশন ও ডিজাইন
st.set_page_config(page_title="YASIN AI SIGNAL V2", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #060606; color: #ffffff; }
    .stSelectbox, .stSlider { background-color: #111; border: 1px solid #ff4b4b; border-radius: 10px; color: white; }
    .signal-card { padding: 40px; border-radius: 20px; text-align: center; border: 2px solid #333; transition: 0.5s; }
    .timer-box { font-size: 24px; color: #f9d423; text-align: center; font-weight: bold; background: #1a1a1a; padding: 10px; border-radius: 12px; border: 1px solid #444; margin-bottom: 15px; }
    .stButton>button { background: linear-gradient(45deg, #ff4b4b, #8b0000); color: white; font-weight: bold; width: 100%; border-radius: 10px; height: 3em; border: none; }
    </style>
    """, unsafe_allow_html=True)

# ২. লগইন সিস্টেম
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🚀 YASIN AI SIGNAL V2</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div style='max-width: 400px; margin: auto; padding: 20px; background: #111; border-radius: 15px; border: 1px solid #ff4b4b;'>", unsafe_allow_html=True)
        user_id = st.text_input("Username", placeholder="Enter Name")
        pass_code = st.text_input("Password", type="password", placeholder="••••••••")
        if st.button("UNLOCK SYSTEM"):
            if pass_code == "Arafat@Vip#Quantum2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Wrong Password!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ৩. সাইডবার সেটিংস ও ২৫টি মার্কেট
st.sidebar.title("💎 VIP CONTROL")
tf_choice = st.sidebar.slider("⏱️ Candle Time (Min)", 1, 30, 1)

markets = {
    "🇪🇺 EUR/USD": "EUR/USD", "🇬🇧 GBP/USD": "GBP/USD", "🇯🇵 USD/JPY": "USD/JPY",
    "🇦🇺 AUD/USD": "AUD/USD", "🇨🇦 USD/CAD": "USD/CAD", "🇨🇭 USD/CHF": "USD/CHF",
    "🇳🇿 NZD/USD": "NZD/USD", "🇪🇺 EUR/GBP": "EUR/GBP", "🇪🇺 EUR/JPY": "EUR/JPY",
    "🇬🇧 GBP/JPY": "GBP/JPY", "🇦🇺 AUD/JPY": "AUD/JPY", "🇪🇺 EUR/AUD": "EUR/AUD",
    "🇪🇺 EUR/CAD": "EUR/CAD", "🇬🇧 GBP/AUD": "GBP/AUD", "🇬🇧 GBP/CAD": "GBP/CAD",
    "🇦🇺 AUD/CAD": "AUD/CAD", "🇨🇦 USD/NOK": "USD/NOK", "🇨🇦 USD/SEK": "USD/SEK",
    "📀 GOLD (XAU/USD)": "BTC/USDT", "🥈 SILVER (XAG/USD)": "ETH/USDT",
    "🛢️ OIL": "USO/USD", "₿ BTC/USDT": "BTC/USDT", "💎 ETH/USDT": "ETH/USDT",
    "🚀 SOL/USDT": "SOL/USDT", "🐕 DOG
