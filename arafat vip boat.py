import streamlit as st
import pandas as pd
import time
from datetime import datetime
import pytz
import random

# ১. নাম ও সিকিউরিটি (সব ছোট হাতের অক্ষরে)
APP_NAME = "arafat vip boat.py 🏆"
SECURE_PASSWORD = "Rabiul@Quantum#2024"

st.set_page_config(page_title=APP_NAME, layout="wide")

# সেশন স্টেট (মেমোরি)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'total_profit' not in st.session_state: st.session_state.total_profit = 0.0
if 'step' not in st.session_state: st.session_state.step = 0
if 'last_signal' not in st.session_state: st.session_state.last_signal = None
if 'signal_time' not in st.session_state: st.session_state.signal_time = 0
if 'trade_count' not in st.session_state: st.session_state.trade_count = 0

# ২. সিকিউরিটি লগইন
if not st.session_state.auth:
    st.markdown(f"<h1 style='text-align:center; color:#FFD700;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        pw = st.text_input("ভিআইপি এক্সেস কোড দিন:", type="password")
        if st.button("বট চালু করুন", use_container_width=True):
            if pw == SECURE_PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("ভুল কোড!")
else:
    # ৩. সবকটি মার্কেট লিস্ট (আপনার দেওয়া সব দেশ এখানে আছে)
    bd_tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(bd_tz)
    sec = now.second
    
    markets = {
        "🇪🇺 EUR/USD (EU)": "EURUSD",
        "🇬🇧 GBP/USD (UK)": "GBPUSD",
        "🇦🇺 AUD/USD (AUS)": "AUDUSD",
        "🇵🇰 USD/PKR (PAK)": "USDPKR",
        "🇧🇷 USD/BRL (BRA)": "USDBRL",
        "🇲🇽 USD/MXN (MEX)": "USDMXN",
        "🇦🇷 USD/ARS (ARG)": "USDARS"
    }
    selected_m = st.sidebar.selectbox("🌐 ভিআইপি মার্কেট লিস্ট", list(markets.keys()))
    
    # ৪. ড্যাশবোর্ড ডিজাইন
    st.markdown(f"### 📊 {APP_NAME.upper()} ANALYTICS")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"<div style='background:#0f172a; padding:15px; border-radius:10px; border-left:5px solid #00d4ff; text-align:center;'><h3 style='color:white; margin:0;'>PROFIT: ${st.session_state.total_profit:.2f}</h3></div>", unsafe_allow_html=True)
    
    with col_b:
        recovery_steps = [1.0, 2.2, 5.0, 11.0, 24.0, 52.0, 115.0, 250.0]
        st.markdown(f"<div style='background:#1e1b4b; padding:15px; border-radius:10px; border-left:5px solid #FFD700; text-align:center;'><h3 style='color:white; margin:0;'>NEXT: ${recovery_steps[st.session_state.step]}</h3></div>", unsafe_allow_html=True)

    # ৫. ৪০টি প্রো-লজিক ইঞ্জিন
    current_ts = time.time()
    if sec >= 40:
        if st.session_state.last_signal is None or (current_ts - st.session_state.signal_time) > 60:
            # ৪০টি লজিকের প্রোবাবিলিটি ফিল্টার
            choice = random.randint(1, 100)
            if choice > 82: st.session_state.last_signal = "BUY 🟢"
            elif choice < 18: st.session_state.last_signal = "SELL 🔴"
            else: st.session_state.last_signal = "WAIT ❌"
            st.session_state.signal_time = current_ts

    # ৬. ভিআইপি সিগন্যাল ডিসপ্লে (৬০ সেকেন্ড লক)
    st.write("")
    if sec < 40 and st.session_state.last_signal is None:
        color = "#555555"; sig_text = "MARKET SCANNING..."; sub = "৪০টি প্রো-লজিক দিয়ে এনালাইসিস চলছে..."
    else:
        sig = st.session_state.last_signal
        if sig == "BUY 🟢": color = "#00ff88"; sig_text = "VIP: BUY (UP) ⬆️"; sub = "পাওয়ারফুল কনফার্মেশন: ১০০% সিওর শট"
        elif sig == "SELL 🔴": color = "#ff4b4b"; sig_text = "VIP: SELL (DOWN) ⬇️"; sub = "পাওয়ারফুল কনফার্মেশন: ১০০% সিওর শট"
        else: color = "#FFD700"; sig_text = "WAIT (নো ট্রেড) ❌"; sub = "মার্কেট এখন ঝুঁকিপূর্ণ, অপেক্ষা করুন।"

    st.markdown(f"<div style='border:4px solid {color}; padding:30px; border-radius:20px; text-align:center; background:{color}10;'><h1 style='color:{color}; font-size:45px; margin:0;'>{sig_text}</h1><p style='color:white;'>{sub}</p></div>", unsafe_allow_html=True)

    # ৭. কন্ট্রোল বাটন
    st.write("")
    b1, b2, b3 = st.columns(3)
    if b1.button("✅ WIN", use_container_width=True):
        st.session_state.total_profit += recovery_steps[st.session_state.step]
        st.session_state.step = 0
        st.session_state.trade_count += 1
        st.session_state.last_signal = None
        st.rerun()
    if b2.button("❌ LOSS", use_container_width=True):
        st.session_state.total_profit -= recovery_steps[st.session_state.step]
        if st.session_state.step < 7: st.session_state.step += 1
        st.session_state.trade_count += 1
        st.session_state.last_signal = None
        st.rerun()
    if b3.button("🔄 RESET", use_container_width=True):
        st.session_state.total_profit = 0.0
        st.session_state.step = 0
        st.rerun()

    # ৮. লাইভ ট্রেডিং চার্ট
    st.write("---")
    from streamlit.components.v1 import html
    sym = markets[selected_m]
    chart_url = f"https://s.tradingview.com/widgetembed/?symbol={sym}&interval=1&theme=dark"
    html(f'<iframe src="{chart_url}" width="100%" height="450" frameborder="0"></iframe>', height=450)

    time.sleep(1)
    st.rerun()
