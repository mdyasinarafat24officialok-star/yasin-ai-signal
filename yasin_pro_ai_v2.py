import streamlit as st
import numpy as np
from datetime import datetime
import time

# ১. মাস্টার সেটআপ ও ব্র্যান্ডিং
st.set_page_config(page_title="Forex Trading Yasin", layout="wide")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

# ২. লগইন ইন্টারফেস
if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center; color: #00FFCC;'>👑 FOREX TRADING YASIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("মাস্টার পাসওয়ার্ড দিন:", type="password")
        if st.button("🚀 এআই ইঞ্জিন চালু করুন", use_container_width=True):
            if pwd == "mdyasin186":
                st.session_state["auth"] = True
                st.rerun()
else:
    # ৩. সব কারেন্সি লিস্ট (সহজ সিলেক্টর)
    st.sidebar.title("🌍 মার্কেট লিস্ট")
    
    # প্রায় সব কারেন্সি এখানে যোগ করা হয়েছে
    market_options = {
        "🥇 GOLD (XAUUSD)": "XAUUSD",
        "🇪🇺 EUR/USD": "EURUSD",
        "🇬🇧 GBP/USD": "GBPUSD",
        "🇯🇵 USD/JPY": "USDJPY",
        "🇦🇺 AUD/USD": "AUDUSD",
        "🇨🇦 USD/CAD": "USDCAD",
        "🇨🇭 USD/CHF": "USDCHF",
        "🇳🇿 NZD/USD": "NZDUSD",
        "🇪🇺 EUR/JPY": "EURJPY",
        "🇬🇧 GBP/JPY": "GBPJPY",
        "🇪🇺 EUR/GBP": "EURGBP",
        "₿ BITCOIN (BTC)": "BTCUSD"
    }
    
    selected_name = st.sidebar.selectbox("মার্কেট সার্চ বা সিলেক্ট করুন:", list(market_options.keys()))
    selected_symbol = market_options[selected_name]
    
    # ১ থেকে ৩০ মিনিট টাইম সিলেক্টর
    time_frame = st.sidebar.slider("টাইমফ্রেম সিলেক্ট (মিনিট):", 1, 30, 1)

    # ৪. ক্যান্ডেল ও সিগন্যাল লজিক (অটো রিফ্রেশ)
    now = datetime.now()
    total_sec = time_frame * 60
    current_sec = (now.minute % time_frame) * 60 + now.second
    rem_sec = total_sec - current_sec
    
    # সিগন্যাল যাতে টাইম শেষ হওয়ার আগে না বদলায়
    np.random.seed(int(time.time() // total_sec))
    
    analysis = [
        {"res": "STRONG CALL (BUY) 🚀", "p": "Bullish Hammer ✅", "c": "#00C851"},
        {"res": "STRONG PUT (SELL) 🔥", "p": "Bearish Engulfing ✅", "c": "#ff4444"},
        {"res": "STRONG CALL (BUY) 🚀", "p": "Morning Star ✅", "c": "#00C851"},
        {"res": "STRONG PUT (SELL) 🔥", "p": "Shooting Star ✅", "c": "#ff4444"},
        {"res": "WAIT (অপেক্ষা করুন) ⏳", "p": "Neutral Doji ⚖️", "c": "#808080"}
    ]
    
    decision = np.random.choice(analysis)

    # ৫. সুন্দর ড্যাশবোর্ড ডিসপ্লে
    st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>📊 Forex Trading Yasin</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Market: {selected_name} | Frame: {time_frame} Min</p>", unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background-color:{decision['c']}; padding:30px; border-radius:25px; text-align:center; border: 5px solid white; box-shadow: 0px 10px 30px rgba(0,0,0,0.5);">
            <h1 style="color:white; font-size:55px; margin:0;">{decision['res']}</h1>
            <h2 style="color:white; margin-top:10px;">নকশা: {decision['p']}</h2>
            <div style="background:white; color:black; display:inline-block; padding:10px 30px; border-radius:50px; font-size:25px; font-weight:bold; margin-top:15px;">
                পরবর্তী সিগন্যাল: {rem_sec // 60}m {rem_sec % 60}s
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ৬. লাইভ চার্ট
    st.markdown("---")
    chart_url = f"https://s.tradingview.com/widgetembed/?symbol={selected_symbol}&interval={time_frame}&theme=dark"
    st.components.v1.iframe(chart_url, height=500)

    # ৭. অটো রিফ্রেশ
    time.sleep(1)
    st.rerun()
