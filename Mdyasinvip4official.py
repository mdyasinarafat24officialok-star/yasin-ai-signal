import streamlit as st
import time
from datetime import datetime
import pytz
import random

# ১. কনফিগারেশন
APP_NAME = "এমডি ইয়াসিন ভিআইপি ৪ (অফিসিয়াল) 💎"
PASSWORD = "mdyasinofficial2023"

st.set_page_config(page_title="Mdyasinvip4official", layout="wide")

# ২. সেশন স্টেট (স্মার্ট মেমোরি)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'total_profit' not in st.session_state: st.session_state.total_profit = 0.0
if 'step' not in st.session_state: st.session_state.step = 0
if 'signal_locked' not in st.session_state: st.session_state.signal_locked = False
if 'current_decision' not in st.session_state: st.session_state.current_decision = "অপেক্ষা করুন"
if 'current_direction' not in st.session_state: st.session_state.current_direction = ""
if 'last_min' not in st.session_state: st.session_state.last_min = -1

# ৩. লগইন প্রোটেকশন
if not st.session_state.auth:
    st.markdown(f"<h1 style='text-align:center; color:#00E676;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        pw = st.text_input("পাসওয়ার্ড দিন:", type="password")
        if st.button("সিস্টেম আনলক করুন", use_container_width=True):
            if pw == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("ভুল পাসওয়ার্ড!")
else:
    # ৪. সাইডবার - মার্কেট ও ১-৩০ টাইম ফ্রেম
    st.sidebar.title("💎 ভিআইপি কন্ট্রোল")
    
    markets = [
        "🇧🇩 USD/BDT (OTC)", "🇮🇳 USD/INR (OTC)", "🇪🇺🇺🇸 EUR/USD", 
        "🇬🇧🇺🇸 GBP/USD", "👑 GOLD (XAUUSD)", "🇧🇷 USD/BRL (OTC)", 
        "🇵🇰 USD/PKR (OTC)", "🥈 SILVER"
    ]
    selected_m = st.sidebar.selectbox("মার্কেট সিলেক্ট করুন:", markets)
    
    # ১ থেকে ৩০ পর্যন্ত সিরিয়াল টাইম ফ্রেম
    time_options = list(range(1, 31))
    time_frame = st.sidebar.selectbox("টাইম ফ্রেম সিলেক্ট করুন (মিনিট):", time_options)
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 সব ডাটা রিসেট"):
        st.session_state.total_profit = 0.0
        st.session_state.step = 0
        st.rerun()

    # ৫. টাইম সেটআপ (বাংলাদেশ সময়)
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz)
    bd_time = now.strftime("%I:%M:%S %p")
    sec = now.second
    min_now = now.minute
    next_trade_min = (min_now + time_frame) % 60

    # ৬. ড্যাশবোর্ড
    st.markdown(f"<h3 style='text-align:center;'>📍 {selected_m} | সময়কাল
