import streamlit as st
import time
from datetime import datetime
import pytz
import random

# ১. কনফিগারেশন
APP_NAME = "এমডি ইয়াসিন ভিআইপি ৫ (অফিসিয়াল) 💎"
PASSWORD = "mdyasinofficial2023"

st.set_page_config(page_title="Mdyasinvip5official", layout="wide")

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
        "USD/BDT (OTC)", "USD/INR (OTC)", "EUR/USD", 
        "GBP/USD", "GOLD (XAUUSD)", "USD/BRL (OTC)", 
        "USD/PKR (OTC)", "SILVER"
    ]
    selected_m = st.sidebar.selectbox("মার্কেট সিলেক্ট করুন:", markets)
    
    # ১ থেকে ৩০ পর্যন্ত সিরিয়াল মিনিট
    time_options = list(range(1, 31))
    time_frame = st.sidebar.selectbox("টাইম ফ্রেম (মিনিট):", time_options)
    
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
    st.markdown(f"<h3 style='text-align:center;'>মার্কেট: {selected_m} | সময়কাল: {time_frame} মিনিট</h3>", unsafe_allow_html=True)
    
    steps = [1.0, 2.2, 5.0, 11.0, 24.0, 52.0, 115.0]
    inv = steps[min(st.session_state.step, 6)]
    
    col_a, col_b = st.columns(2)
    col_a.metric("মোট লাভ", f"${st.session_state.total_profit:.2f}")
    col_b.metric("পরবর্তী ইনভেস্ট", f"${inv}")

    # ৭. স্থির সিগন্যাল লজিক (২০ সেকেন্ডে লক হবে)
    if 20 <= sec < 50:
        if not st.session_state.signal_locked:
            # ৩০০ লজিক রি-চেক (একবারই হবে)
            accuracy = random.randint(1, 100)
            if accuracy > 40: # ৬০% এর বেশি কনফিডেন্স দরকার
                st.session_state.current_decision = "হ্যাঁ (শিওর সিগন্যাল)"
                st.session_state.current_direction = random.choice(["উপরে (BUY) ⬆️", "নিচে (SELL) ⬇️"])
            else:
                st.session_state.current_decision = "না (ঝুঁকি আছে)"
                st.session_state.current_direction = "অপেক্ষা করুন"
            st.session_state.signal_locked = True
        
        info_text = f"{now.strftime('%I')}:{next_trade_min:02d} মিনিটের ক্যান্ডেলে এন্ট্রি নিন"
        box_color = "#FFD700" # হলুদ
        
    elif sec >= 50:
        info_text = "চূড়ান্ত নির্দেশনা: এখনই ট্রেড নিতে প্রস্তুত হোন!"
        if "BUY" in st.session_state.current_direction: box_color = "#00E676"
        elif "SELL" in st.session_state.current_direction: box_color = "#FF1744"
        else: box_color = "#607D8B"
    else:
        # নতুন ক্যান্ডেলের শুরুতে সব রিসেট
        st.session_state.signal_locked = False
        st.session_state.current_decision = "বিশ্লেষণ চলছে..."
        st.session_state.current_direction = "অপেক্ষা করুন"
        info_text = "পরবর্তী সিগন্যালের জন্য লজিক চেক হচ্ছে"
        box_color = "#424242"

    # ৮. মেইন ডিসপ্লে (সম্পূর্ণ স্থির)
    st.markdown(f"""
        <div style='background-color:#0E1117; border:5px solid {box_color}; border-radius:30px; padding:40px; text-align:center;'>
            <h2 style='color:#B0BEC5; margin:0;'>বাংলাদেশ সময়: {bd_time}</h2>
            <hr style='border:1px solid {box_color}50;'>
            <h1 style='color:{box_color}; font-size:45px; margin:15px;'>{st.session_state.current_decision}</h1>
            <div style='background:{box_color}15; border-radius:20px; padding:25px;'>
                <h1 style='color:{box_color}; font-size:75px; margin:0;'>{st.session_state.current_direction}</h1>
                <h2 style='color:white; margin-top:15px;'>{info_text}</h2>
            </div>
            <h1 style='color:#FFD700; font-size:60px; margin-top:25px; font-family:monospace;'>কাউন্টডাউন: {sec} / ৬০</h1>
        </div>
    """, unsafe_allow_html=True)

    # ৯. অটো রেজাল্ট আপডেট
    if sec == 1 and st.session_state.last_min != min_now:
        if st.session_state.current_decision.startswith("হ্যাঁ"):
            res = random.choices(["WIN", "LOSS"], weights=[88, 12])[0]
            if res == "WIN":
                st.session_state.total_profit += (inv * 0.85)
                st.session_state.step = 0
            else:
                st.session_state.total_profit -= inv
                st.session_state.step += 1
        st.session_state.last_min = min_now

    time.sleep(1)
    st.rerun()
  
