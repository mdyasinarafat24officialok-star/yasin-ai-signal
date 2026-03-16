import streamlit as st
import streamlit.components.v1 as components
import random
import time
from datetime import datetime

# ১. অ্যাপ কনফিগারেশন (সব ছোট হাতের অক্ষর ও ইউনিক নাম)
app_name = "aryan quantum-z pro vip 👑"
secure_password = "aryan@vip#2026_x"

st.set_page_config(page_title=app_name, layout="wide")

# ২. ডিজাইন (CSS)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050a0f; color: #ffffff; }}
    .main-card {{
        background: linear-gradient(145deg, #0d1b2a, #162331);
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #00ffcc;
        text-align: center;
        margin-bottom: 10px;
    }}
    .signal-box {{
        font-size: 32px;
        font-weight: bold;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        border: 2px solid #ffffff;
    }}
    .money-box {{
        background-color: #1b263b;
        padding: 10px;
        border-radius: 8px;
        border-left: 5px solid #ffcc00;
        margin-bottom: 10px;
    }}
    .stButton>button {{
        width: 100%;
        background-color: #1b263b;
        color: #00ffcc !important;
        border: 1px solid #00ffcc;
        font-weight: bold;
        border-radius: 8px;
        height: 3.5em;
    }}
    </style>
    """, unsafe_allow_html=True)

# ৩. সেশন স্টেট (ডাটা মনে রাখার লজিক)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'step' not in st.session_state: st.session_state.step = 0
if 'm_selected' not in st.session_state: st.session_state.m_selected = None

# ৮টি ধাপের রিকভারি চার্ট (৮ ধাপের হিসাব)
recovery_steps = [1, 2.2, 5, 11, 24, 52, 115, 250]

# ৪. লগইন সিস্টেম
if not st.session_state.auth:
    st.markdown(f"<h1 style='text-align: center; color: #00ffcc;'>{app_name.upper()}</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        pw = st.text_input("পাসওয়ার্ড দিন", type="password")
        if st.button("প্রবেশ করুন"):
            if pw == secure_password:
                st.session_state.auth = True
                st.rerun()
            else: st.error("ভুল পাসওয়ার্ড!")
else:
    # ৫. হেডার ও লাইভ টাইম
    h_col1, h_col2 = st.columns([2, 1])
    with h_col1:
        st.markdown(f"<h3 style='color:#00ffcc; margin:0;'>{app_name.upper()}</h3>", unsafe_allow_html=True)
    with h_col2:
        now = datetime.now().strftime("%H:%M:%S")
        st.markdown(f"<p style='color:#ffcc00; text-align:right;'>🕒 {now}</p>", unsafe_allow_html=True)

    # ৬. মানি ম্যানেজমেন্ট (অটো রিকভারি)
    st.markdown(f"""
    <div class='money-box'>
        💰 বর্তমান ট্রেড: <b>${recovery_steps[st.session_state.step]}</b><br>
        📊 রিকভারি ধাপ: {st.session_state.step + 1} / 8
    </div>
    """, unsafe_allow_html=True)

    # ৭. মার্কেট সিলেকশন (আপনার দেওয়া লিস্ট)
    markets = {
        "🇵🇰 usd/pkr": "usdpkr", "🇲🇽 usd/mxn": "usdmxn", "🇧🇷 usd/brl": "usdbrl",
        "🇳🇿 usd/nzd": "usdnzd", "🇨🇴 usd/cop": "usdcop", "🇦🇷 usd/ars": "usdars", "🇩🇿 usd/dzd": "usddzd"
    }
    
    st.write("🌐 মার্কেট সিলেক্ট করুন:")
    m_cols = st.columns(4)
    for i, (m_name, m_sym) in enumerate(markets.items()):
        if m_cols[i % 4].button(m_name.upper()):
            st.session_state.m_selected = m_name
            st.session_state.m_symbol = m_sym
            st.session_state.start_time = time.time()
            st.session_state.scan = True

    # ৮. সিগন্যাল ইঞ্জিন ও টাইমার
    if st.session_state.m_selected:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        
        # টাইমার লজিক
        remaining = 60 - (int(time.time() - st.session_state.start_time) % 60)
        st.markdown(f"<h2 style='color:#ffcc00; margin:0;'>⏳ {remaining}s</h2>", unsafe_allow_html=True)
        st.write(f"মার্কেট: **{st.session_state.m_selected.upper()}**")

        if st.session_state.get('scan', False):
            with st.spinner('এনালাইসিস চলছে...'):
                time.sleep(2)
                res = random.choice(["হ্যাঁ - buy (up) ✅", "হ্যাঁ - sell (down) ✅", "না - অপেক্ষা করুন ❌"])
                st.session_state.last_res = res
                st.session_state.scan = False
        
        if 'last_res' in st.session_state:
            sig = st.session_state.last_res
            s_color = "#00ff88" if "buy" in sig else "#ff4a4a" if "sell" in sig else "#ffffff"
            st.markdown(f"<div class='signal-box' style='color:{s_color}; border-color:{s_color};'>{sig.upper()}</div>", unsafe_allow_html=True)

        # রেজাল্ট বাটন
        res_col1, res_col2 = st.columns(2)
        if res_col1.button("✅ লাভ (win)"):
            st.session_state.step = 0 # ১ ডলারে ব্যাক
            st.rerun()
        if res_col2.button("❌ লস (loss)"):
            if st.session_state.step < 7:
                st.session_state.step += 1 # পরের ধাপ
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

    # ৯. চার্ট (ট্রেডিং ভিউ)
    target = st.session_state.get('m_symbol', 'usdbrl')
    tv_code = f"""
    <iframe src="https://s.tradingview.com/widgetembed/?symbol={target.upper()}&interval=1&theme=dark" width="100%" height="450" frameborder="0"></iframe>
    """
    components.html(tv_code, height=450)

    # ১০. লাইভ রিফ্রেশ
    if st.session_state.m_selected:
        time.sleep(1)
        st.rerun()
