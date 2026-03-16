import streamlit as st
import streamlit.components.v1 as components
import random
import time
from datetime import datetime

# ১. ইউনিক নাম ও পাসওয়ার্ড
APP_NAME = "ARIAN QUANTUM VIP BOT 👑"
SECURE_PASSWORD = "Aryan@VIP#2026_X"

st.set_page_config(page_title=APP_NAME, layout="wide")

# ২. ইউনিক ডিজাইন (CSS)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050a0f; color: #ffffff; }}
    .main-card {{
        background: linear-gradient(145deg, #0d1b2a, #1b263b);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #00ffcc;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
    }}
    .stButton>button {{
        width: 100%;
        background-color: #1b263b;
        color: #00ffcc !important;
        border: 1px solid #00ffcc;
        border-radius: 10px;
        height: 3.5em;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: #00ffcc;
        color: #050a0f !important;
    }}
    .clock-text {{ font-size: 22px; color: #ffcc00; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# ৩. লগইন সিস্টেম
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown(f"<h1 style='text-align: center; color: #00ffcc;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        user_input = st.text_input("সিকিউরিটি কি (Key) দিন", type="password")
        if st.button("ড্যাশবোর্ড আনলক করুন"):
            if user_input == SECURE_PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("ভুল কি! আবার চেষ্টা করুন।")
else:
    # ৪. লাইভ ঘড়ি ও হেডার
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"<h2 style='color: #00ffcc;'>{APP_NAME} AI ড্যাশবোর্ড</h2>", unsafe_allow_html=True)
    with c2:
        now = datetime.now().strftime("%H:%M:%S")
        st.markdown(f"<div class='clock-text'>🕒 সময়: {now}</div>", unsafe_allow_html=True)

    # ৫. মার্কেট বাটন (লোগো সহ)
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    markets = {
        "💎 EUR/USD (OTC)": "EURUSD",
        "💎 GBP/USD (OTC)": "GBPUSD",
        "💎 USD/JPY (OTC)": "USDJPY",
        "💎 AUD/CAD (OTC)": "AUDCAD",
        "💎 Crypto IDX": "BTCUSD"
    }
    
    cols = st.columns(len(markets))
    m_names = list(markets.keys())
    
    for i in range(len(m_names)):
        if cols[i].button(m_names[i]):
            st.session_state.m_name = m_names[i]
            st.session_state.m_symbol = markets[m_names[i]]
            st.session_state.scan = True

    # ৬. সিগন্যাল এনালাইসিস
    if 'm_name' in st.session_state:
        st.write(f"সিলেক্টেড মার্কেট: **{st.session_state.m_name}**")
        if st.session_state.get('scan', False):
            with st.spinner('কোয়ান্টাম এনালাইসিস চলছে...'):
                time.sleep(2)
                res = random.choice(["CALL (UP) 🟢", "PUT (DOWN) 🔴", "WAIT (RISKY) ⚪"])
                st.session_state.last_res = res
                st.session_state.scan = False
        
        if 'last_res' in st.session_state:
            color = "#00ff88" if "CALL" in st.session_state.last_res else "#ff4a4a" if "PUT" in st.session_state.last_res else "#ffffff"
            st.markdown(f"<h1 style='color: {color}; font-size: 60px;'>{st.session_state.last_res}</h1>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ৭. ট্রেডিং ভিউ লাইভ চার্ট
    st.markdown("### 📊 TradingView লাইভ চার্ট")
    target = st.session_state.get('m_symbol', 'EURUSD')
    tv_code = f"""
    <iframe src="https://s.tradingview.com/widgetembed/?symbol={target}&interval=1&theme=dark" width="100%" height="550" frameborder="0"></iframe>
    """
    components.html(tv_code, height=550)
