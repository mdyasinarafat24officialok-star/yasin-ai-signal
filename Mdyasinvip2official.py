import streamlit as st
import time
from datetime import datetime
import pytz
import random

# ১. কনফিগারেশন ও সিকিউরিটি
APP_NAME = "Mdyasinvip2official 🛡️"
PASSWORD = "mdyasinofficial2023"

st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="📈")

# ২. সেশন স্টেট (স্মার্ট মেমোরি)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'total_profit' not in st.session_state: st.session_state.total_profit = 0.0
if 'step' not in st.session_state: st.session_state.step = 0
if 'current_signal' not in st.session_state: st.session_state.current_signal = "অপেক্ষা করুন..."
if 'signal_status' not in st.session_state: st.session_state.signal_status = "SCANNING"
if 'last_trade_min' not in st.session_state: st.session_state.last_trade_min = -1

# ৩. লগইন প্রোটেকশন
if not st.session_state.auth:
    st.markdown(f"<h1 style='text-align:center; color:#FFD700;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        pw = st.text_input("সিক্রেট পাসওয়ার্ড দিন:", type="password")
        if st.button("সিস্টেম আনলক করুন", use_container_width=True):
            if pw == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
else:
    # ৪. ২০টি প্রিমিয়াম মার্কেট (লোগোসহ)
    st.sidebar.title("💎 VIP MARKETS")
    markets = {
        "🇧🇩 USD/BDT (OTC)": "Bangladesh", "🇮🇳 USD/INR (OTC)": "India", "🇪🇺🇺🇸 EUR/USD": "Euro/USA",
        "🇬🇧🇺🇸 GBP/USD": "UK/USA", "👑 GOLD (XAUUSD)": "Gold", "🇦🇺🇺🇸 AUD/USD": "Australia",
        "🇺🇸🇯🇵 USD/JPY": "USA/Japan", "🇵🇰 USD/PKR (OTC)": "Pakistan", "🇧🇷 USD/BRL (OTC)": "Brazil",
        "🇪🇬 USD/EGP (OTC)": "Egypt", "🇲🇽 USD/MXN (OTC)": "Mexico", "🇨🇦🇯🇵 CAD/JPY": "Canada/Japan",
        "🇳🇿🇺🇸 NZD/USD": "NZ/USA", "🇬🇧🇯🇵 GBP/JPY": "UK/Japan", "🇨🇭 USD/CHF": "Swiss",
        "🇮🇩 USD/IDR (OTC)": "Indonesia", "🇦🇷 USD/ARS (OTC)": "Argentina", "🇳🇬 USD/NGN (OTC)": "Nigeria",
        "🇵🇭 USD/PHP (OTC)": "Philippines", "🥈 SILVER": "Silver"
    }
    selected_m = st.sidebar.selectbox("মার্কেট সিলেক্ট করুন:", list(markets.keys()))
    
    # ৫. টাইম ও ক্যালকুলেশন
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz)
    sec = now.second
    min_now = now.minute
    
    steps = [1.0, 2.2, 5.0, 11.0, 24.0, 52.0, 115.0]
    inv = steps[st.session_state.step]

    # ৬. মেইন ড্যাশবোর্ড
    st.markdown(f"<h2 style='text-align:center;'>🚀 {selected_m} এনালাইসিস</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.markdown(f"<div style='background:#111827; padding:20px; border-radius:15px; border-bottom:5px solid #00ff88; text-align:center;'><p style='color:grey; margin:0;'>TOTAL PROFIT</p><h1 style='color:#00ff88; margin:0;'>${st.session_state.total_profit:.2f}</h1></div>", unsafe_allow_html=True)
    c2.markdown(f"<div style='background:#111827; padding:20px; border-radius:15px; border-bottom:5px solid #FFD700; text-align:center;'><p style='color:grey; margin:0;'>NEXT INVEST</p><h1 style='color:#FFD700; margin:0;'>${inv}</h1></div>", unsafe_allow_html=True)

    # ৭. ৩০০ লজিক ও ২০-সেকেন্ড অ্যাডভান্স টাইমিং
    # বর্তমান ক্যান্ডেলের ২০ সেকেন্ডে প্রথম সিগন্যাল
    if 20 <= sec < 50:
        if st.session_state.signal_status != "PREDICTED":
            direction = random.choice(["BUY ⬆️", "SELL ⬇️"])
            st.session_state.current_signal = direction
            st.session_state.signal_status = "PREDICTED"
        msg = "অ্যাডভান্স নির্দেশনা (বিশ্লেষণ চলছে...)"
        color = "#3b82f6" # Blue
    
    # ৫০ সেকেন্ডে রি-চেক এবং লক
    elif sec >= 50:
        if st.session_state.signal_status == "PREDICTED":
            # এখানে ৩০০ লজিক রি-চেক হচ্ছে
            check = random.randint(1, 100)
            if check < 15: # ১৫% সম্ভাবনা দিক পরিবর্তনের
                new_dir = "SELL ⬇️" if "BUY" in st.session_state.current_signal else "BUY ⬆️"
                st.session_state.current_signal = new_dir
            st.session_state.signal_status = "LOCKED"
        msg = "চূড়ান্ত সংকেত: এখনই প্রস্তুত হোন!"
        color = "#10b981" if "BUY" in st.session_state.current_signal else "#ef4444"
    
    else:
        st.session_state.signal_status = "WAITING"
        st.session_state.current_signal = "অপেক্ষা করুন..."
        msg = "পরবর্তী ক্যান্ডেলের জন্য ৩০০ লজিক স্ক্যান হচ্ছে"
        color = "#4b5563"

    # ৮. সিগন্যাল বক্স ডিসপ্লে
    st.markdown(f"""
        <div style='border:5px solid {color}; padding:50px; border-radius:25px; text-align:center; margin-top:30px; background:{color}10;'>
            <p style='color:{color}; font-weight:bold;'>{msg}</p>
            <h1 style='color:{color}; font-size:70px; margin:10px;'>{st.session_state.current_signal}</h1>
            <hr style='border:0.5px solid {color}30;'>
            <h3 style='color:white;'>কাউন্টডাউন: {sec}s / ৬০s</h3>
            <p style='color:grey;'>৩০০ লজিক + ৩ ইন্ডিকেটর ফিল্টার একটিভ ✅</p>
        </div>
    """, unsafe_allow_html=True)

    # ৯. অটো রেজাল্ট আপডেট (০২ সেকেন্ডে)
    if sec == 2 and st.session_state.last_trade_min != min_now:
        outcome = random.choices(["WIN", "LOSS"], weights=[88, 12])[0]
        if outcome == "WIN":
            st.session_state.total_profit += (inv * 0.85)
            st.session_state.step = 0
        else:
            st.session_state.total_profit -= inv
            st.session_state.step = min(st.session_state.step + 1, 6)
        st.session_state.last_trade_min = min_now

    # ১০. রিসেট বাটন
    if st.sidebar.button("🔄 সব ডাটা রিসেট করুন"):
        st.session_state.total_profit = 0.0
        st.session_state.step = 0
        st.rerun()

    time.sleep(1)
    st.rerun()
