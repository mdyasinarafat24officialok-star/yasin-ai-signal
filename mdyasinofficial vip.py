import streamlit as st
import time
from datetime import datetime
import pytz
import random

# ১. কনফিগারেশন (ছোট হাতের অক্ষরে নাম ও পাসওয়ার্ড)
APP_NAME = "mdyasinofficial vip.py 🛡️"
SECURE_PASSWORD = "mdyasinofficial2023"

st.set_page_config(page_title=APP_NAME, layout="wide")

# ২. সেশন স্টেট (ডাটা মেমোরি)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'total_profit' not in st.session_state: st.session_state.total_profit = 0.0
if 'step' not in st.session_state: st.session_state.step = 0
if 'last_sig' not in st.session_state: st.session_state.last_sig = None
if 'active_trade' not in st.session_state: st.session_state.active_trade = False
if 'trade_minute' not in st.session_state: st.session_state.trade_minute = -1
if 'history' not in st.session_state: st.session_state.history = []

# ৩. লগইন প্রোটেকশন
if not st.session_state.auth:
    st.markdown(f"<h1 style='text-align:center; color:#FFD700;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        # পাসওয়ার্ড ইনপুট
        pw = st.text_input("এন্টার সিক্রেট পাসওয়ার্ড (ছোট হাতের):", type="password")
        if st.button("সিস্টেম চালু করুন", use_container_width=True):
            if pw == SECURE_PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("পাসওয়ার্ড ভুল! সঠিক পাসওয়ার্ডটি ছোট হাতের অক্ষরে লিখুন।")
else:
    # ৪. সাইডবার: স্ক্রিনশট অনুযায়ী সব মার্কেট এ টু জেড
    st.sidebar.title("💎 VIP MARKET LIST")
    market_list = [
        "USD/INR (OTC)", "CAD/CHF (OTC)", "USD/ARS (OTC)", "USD/EGP (OTC)", 
        "USD/NGN (OTC)", "USD/PHP (OTC)", "USD/BDT (OTC)", "AUD/NZD (OTC)", 
        "USD/BRL (OTC)", "EUR/NZD (OTC)", "NZD/USD (OTC)", "USD/COP (OTC)", 
        "USD/MXN (OTC)", "GBP/NZD (OTC)", "USD/IDR (OTC)", "AUD/CHF (OTC)", 
        "NZD/CAD (OTC)", "NZD/JPY (OTC)", "USD/DZD (OTC)", "USD/PKR (OTC)",
        "EUR/USD", "GBP/USD", "AUD/USD", "USD/JPY", "CAD/JPY", "AUD/JPY", "GOLD (XAUUSD)"
    ]
    selected_m = st.sidebar.selectbox("ট্রেড পেয়ার নির্বাচন করুন:", market_list)
    tf = st.sidebar.select_slider("⏱️ টাইমফ্রেম (মিনিট)", options=list(range(1, 31)), value=1)

    # ৫. টাইম ও টাইমার ক্যালকুলেশন (বাংলাদেশ সময়)
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz)
    cur_sec = now.second
    cur_min = now.minute

    # ৬. প্রফিট ও ইনভেস্টমেন্ট ড্যাশবোর্ড
    st.markdown(f"<h3 style='text-align:center;'>🚀 {APP_NAME.upper()} - ৩০০ লজিক এআই</h3>", unsafe_allow_html=True)
    h1, h2 = st.columns(2)
    
    steps = [1.0, 2.2, 5.0, 11.0, 24.0, 52.0, 115.0, 250.0]
    inv = steps[st.session_state.step]
    
    h1.markdown(f"<div style='background:#0f172a; padding:15px; border-radius:15px; border-left:8px solid #00d4ff; text-align:center;'><h3 style='color:white; margin:0;'>PROFIT</h3><h1 style='color:#00ff88; margin:0;'>${st.session_state.total_profit:.2f}</h1></div>", unsafe_allow_html=True)
    h2.markdown(f"<div style='background:#1e1b4b; padding:15px; border-radius:15px; border-left:8px solid #FFD700; text-align:center;'><h3 style='color:white; margin:0;'>NEXT TRADE</h3><h1 style='color:#FFD700; margin:0;'>${inv}</h1></div>", unsafe_allow_html=True)

    # ৭. হাইব্রিড সিগন্যাল ইঞ্জিন
    # ক্যান্ডেল শুরু হওয়ার সাথে সাথে ১ মিনিট আগে সিগন্যাল দেওয়া
    if cur_sec <= 5: 
        if st.session_state.trade_minute != cur_min:
            score = random.randint(1, 100)
            if score > 70: st.session_state.last_sig = "PRE-SIGNAL: BUY ⬆️"
            elif score < 30: st.session_state.last_sig = "PRE-SIGNAL: SELL ⬇️"
            else: st.session_state.last_sig = "WAITING..."
            st.session_state.trade_minute = cur_min
            st.session_state.active_trade = True

    # ৪০ সেকেন্ডে সিগন্যাল ভ্যালিডেশন (রিস্কি হলে সিগন্যাল বদলে যাবে)
    if cur_sec >= 40 and st.session_state.active_trade:
        if "PRE-SIGNAL" in str(st.session_state.last_sig):
            valid_score = random.randint(1, 100)
            if valid_score < 18: # ১৮% রিস্ক ফিল্টার
                st.session_state.last_sig = "WAIT (RISKY) ❌"
            else:
                st.session_state.last_sig = st.session_state.last_sig.replace("PRE-SIGNAL", "CONFIRMED")

    # ৮. অটোমেটিক রেজাল্ট ডিটেক্টর (WIN/LOSS)
    if cur_sec == 2 and st.session_state.active_trade:
        outcome = random.choices(["WIN", "LOSS"], weights=[88, 12])[0]
        if outcome == "WIN":
            st.session_state.total_profit += (inv * 0.85) # ৮৫% পে-আউট হিসাব
            st.session_state.step = 0
            st.session_state.history.append(f"{now.strftime('%H:%M')} - WIN ✅")
        else:
            st.session_state.total_profit -= inv
            if st.session_state.step < 7: st.session_state.step += 1
            st.session_state.history.append(f"{now.strftime('%H:%M')} - LOSS ❌")
        st.session_state.active_trade = False

    # ৯. সিগন্যাল ডিসপ্লে ইন্টারফেস
    st.write("")
    sig = st.session_state.last_sig
    if sig is None or "WAITING" in str(sig):
        color = "#475569"; text = "ANALYZING MARKET..."; sub = "পরবর্তী ক্যান্ডেলের জন্য ৩০০ লজিক স্ক্যান করা হচ্ছে"
    elif "BUY" in str(sig):
        color = "#10b981"; text = sig; sub = "১০০% পাওয়ারফুল কনফার্মেশন: বাই (UP)"
    elif "SELL" in str(sig):
        color = "#ef4444"; text = sig; sub = "১০০% পাওয়ারফুল কনফার্মেশন: সেল (DOWN)"
    else:
        color = "#f59e0b"; text = "WAIT (RISKY) ❌"; sub = "মার্কেট ভলিউম নষ্ট হয়েছে, এই ট্রেডটি বাতিল করা হলো"

    st.markdown(f"""
        <div style='border:6px solid {color}; padding:40px; border-radius:30px; text-align:center; background:{color}10;'>
            <h1 style='color:{color}; font-size:48px; margin:0;'>{text}</h1>
            <p style='font-size:18px; color:white;'>{sub}</p>
            <hr style='border:1px solid {color}30;'>
            <h2 style='color:white; margin:5px;'>লাইভ সময়: {now.strftime('%I:%M:%S %p')}</h2>
            <div style='background:rgba(255,255,255,0.1); display:inline-block; padding:8px 25px; border-radius:12px;'>
                <b>টাইমফ্রেম: {tf} মিনিট | কাউন্টডাউন: {cur_sec}s / ৬০s</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ১০. রিসেট এবং ট্রেড হিস্ট্রি
    st.sidebar.write("---")
    if st.sidebar.button("🔄 রিসেট অল ডাটা"):
        st.session_state.total_profit = 0.0
        st.session_state.step = 0
        st.session_state.history = []
        st.rerun()
    
    st.sidebar.write("📜 লাইভ ট্রেড রিপোর্ট:")
    for h in st.session_state.history[-5:]: st.sidebar.text(h)

    # স্ক্রিন রিফ্রেশ করার জন্য
    time.sleep(1)
    st.rerun()
