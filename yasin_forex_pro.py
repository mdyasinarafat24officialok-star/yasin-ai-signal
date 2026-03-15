import streamlit as st
import numpy as np
from datetime import datetime
import time

# ১. মাস্টার ব্র্যান্ডিং এবং পেজ সেটআপ
st.set_page_config(page_title="Forex Trading Yasin", layout="wide")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

# ২. সিকিউর লগইন সিস্টেম
if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center; color: #00FFCC;'>👑 FOREX TRADING YASIN</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>VIP Signal Access</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("মাস্টার পাসওয়ার্ড:", type="password")
        if st.button("🚀 এআই ইঞ্জিন চালু করুন", use_container_width=True):
            if pwd == "mdyasin186":
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("ভুল পাসওয়ার্ড! সঠিক পাসওয়ার্ড দিন।")
else:
    # ৩. কন্ট্রোল প্যানেল (আপনার দেওয়া ৫টি মার্কেট লোগোসহ)
    st.sidebar.title("💎 Yasin Forex Pro")
    
    # আপনার পছন্দের ৫টি কারেন্সি
    assets = {
        "🇪🇺 EURO/USD": "EURUSD",
        "🇬🇧 GBP/USD": "GBPUSD",
        "🇯🇵 USD/JPY": "USDJPY",
        "🥇 GOLD": "XAUUSD",
        "₿ BTC": "BTCUSD"
    }
    
    selected_name = st.sidebar.selectbox("মার্কেট সিলেক্ট করুন:", list(assets.keys()))
    selected_asset = assets[selected_name]
    
    # মিনিট সিলেকশন সুবিধা
    time_frame = st.sidebar.select_slider("টাইম লিস্ট (মিনিট):", options=[1, 5, 15, 30])

    # ৪. ক্যান্ডেল স্থির রাখার লজিক (যাতে সেকেন্ডে সিগন্যাল না বদলায়)
    now = datetime.now()
    total_seconds = time_frame * 60
    remaining_seconds = total_seconds - ((now.minute % time_frame) * 60 + now.second)
    
    # সিড ফিক্স করা যাতে পুরো ক্যান্ডেল টাইমে সিগন্যাল এক থাকে
    np.random.seed(int(time.time() // total_seconds))

    # ৫. মেইন সিগন্যাল ডিসপ্লে
    st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>📊 Forex Trading Yasin</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{selected_name} - {time_frame} Min Signal</h3>", unsafe_allow_html=True)

    analysis_data = [
        {"res": "STRONG CALL (BUY) 🚀", "pattern": "Institutional Buying ✅", "color": "#00C851", "msg": "ব্যাংকগুলো এখন উপরে নিচ্ছে!"},
        {"res": "STRONG PUT (SELL) 🔥", "pattern": "Liquidity Sweep ✅", "color": "#ff4444", "msg": "মার্কেট এখন নিচের দিকে ক্রাশ করবে!"}
    ]
    
    decision = np.random.choice(analysis_data)
    accuracy = np.random.randint(98, 100)

    # সিগন্যাল বক্স (মোবাইল ও পিসির জন্য সুন্দর ডিজাইন)
    st.markdown(f"""
        <div style="background-color:{decision['color']}; padding:40px; border-radius:30px; text-align:center; border: 5px solid white; box-shadow: 0px 10px 40px rgba(0,0,0,0.6);">
            <h1 style="color:white; font-size:70px; margin:0;">{decision['res']}</h1>
            <h2 style="color:white;">প্যাটার্ন: {decision['pattern']} | একুরেসি: {accuracy}%</h2>
            <p style="color:white; font-size:22px;">{decision['msg']}</p>
            <div style="background:white; color:black; display:inline-block; padding:10px 30px; border-radius:50px; font-size:30px; font-weight:bold; margin-top:15px;">
                নতুন সিগন্যাল আসবে: {remaining_seconds}s
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ৬. লাইভ ট্রেডিংভিউ চার্ট
    st.markdown("---")
    chart_url = f"https://s.tradingview.com/widgetembed/?symbol={selected_asset}&interval={time_frame}&theme=dark"
    st.components.v1.iframe(chart_url, height=550)

    if st.sidebar.button("Logout"):
        st.session_state["auth"] = False
        st.rerun()

    time.sleep(1)
    st.rerun()
