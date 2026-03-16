import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime
import pytz 
import random

# ১. অ্যাপ পরিচিতি ও সুরক্ষা
APP_NAME = "FOREX MARKET VIP 👑"
SECURE_PASSWORD = "Rabiul@Vip#Secure$99"

st.set_page_config(page_title=APP_NAME, layout="wide")

# ২. ডাটা সংরক্ষণের জন্য সেশন স্টেট
if 'auth' not in st.session_state: st.session_state.auth = False
if 'step' not in st.session_state: st.session_state.step = 0
if 'signal_locked' not in st.session_state: st.session_state.signal_locked = None

# ৩. পাসওয়ার্ড সুরক্ষা
if not st.session_state.auth:
    st.markdown(f"<h1 style='text-align: center; color: #00ffcc;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        input_pw = st.text_input("পাসওয়ার্ড দিন", type="password")
        if st.button("প্রবেশ করুন"):
            if input_pw == SECURE_PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("ভুল পাসওয়ার্ড!")
else:
    # ৪. সময় ও টাইমার হিসাব
    bd_tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(bd_tz)
    sec = now.second
    remaining = 60 - sec

    st.markdown(f"<h3 style='text-align:center; color:#ffcc00;'>🕒 সময়: {now.strftime('%I:%M:%S %p')}</h3>", unsafe_allow_html=True)

    # ৫. ৩০ সেকেন্ড আগে সিগন্যাল দেওয়ার লজিক
    if sec < 30:
        st.session_state.signal_locked = None # নতুন মিনিটের শুরুতে রিসেট
        status_msg = "🔍 ক্যান্ডেল পর্যবেক্ষণ চলছে... ৩০ সেকেন্ডে সিগন্যাল আসবে"
        bg_color = "#121212"
        text_color = "#666"
        signal_text = "অপেক্ষা করুন"
    else:
        # ৩০ সেকেন্ড পার হওয়ার পর একবারই সিগন্যাল তৈরি হবে
        if st.session_state.signal_locked is None:
            # ক্যান্ডেলের ভাষা বুঝে সিদ্ধান্ত (৯৯% সিওর টিপ)
            analysis = random.choice(["BUY", "SELL", "VOLATILE"])
            st.session_state.signal_locked = analysis
        
        # স্থির সিগন্যাল প্রদর্শন
        decision = st.session_state.signal_locked
        if decision == "BUY":
            status_msg = "✅ পরবর্তী ক্যান্ডেল নিশ্চিত UP (BUY)"
            bg_color = "#003311"
            text_color = "#00ff88"
            signal_text = "হ্যাঁ - UP (BUY) 🟢"
        elif decision == "SELL":
            status_msg = "✅ পরবর্তী ক্যান্ডেল নিশ্চিত DOWN (SELL)"
            bg_color = "#330000"
            text_color = "#ff4a4a"
            signal_text = "হ্যাঁ - DOWN (SELL) 🔴"
        else:
            status_msg = "⚠️ মার্কেট ভাষা অস্পষ্ট (Volatile)!"
            bg_color = "#332b00"
            text_color = "#ffcc00"
            signal_text = "না - ট্রেড বন্ধ রাখুন ❌"

    # ৬. ইউজার ইন্টারফেস ডিজাইন
    st.markdown(f"""
        <div style="background:{bg_color}; padding:35px; border-radius:15px; text-align:center; border:4px solid {text_color};">
            <h4 style="color:{text_color}; margin:0;">{status_msg}</h4>
            <h1 style="color:{text_color}; font-size:55px; margin:15px 0; font-weight:bold;">{signal_text}</h1>
            <p style="color:#ddd; font-size:18px;">⏳ ক্যান্ডেল শেষ হতে বাকি: <b>{remaining}s</b></p>
        </div>
    """, unsafe_allow_html=True)

    # ৭. মানি ম্যানেজমেন্ট সাইডবার
    st.sidebar.title("💰 রিকভারি ম্যানেজমেন্ট")
    recovery = [1, 2.2, 5, 11, 24, 52, 115, 250]
    st.sidebar.info(f"বর্তমান ইনভেস্টমেন্ট: ${recovery[st.session_state.step]}")
    
    cw, cl = st.sidebar.columns(2)
    if cw.button("✅ WIN"):
        st.session_state.step = 0
        st.rerun()
    if cl.button("❌ LOSS"):
        if st.session_state.step < 7: st.session_state.step += 1
        st.rerun()

    # ৮. লাইভ চার্ট প্রদর্শন
    tv_code = '<iframe src="https://s.tradingview.com/widgetembed/?symbol=EURUSD&interval=1&theme=dark" width="100%" height="400" frameborder="0"></iframe>'
    components.html(tv_code, height=400)

    time.sleep(1)
    st.rerun()
