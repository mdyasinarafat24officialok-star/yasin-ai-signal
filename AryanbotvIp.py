import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ১. পেজ সেটআপ (এটি সবার আগে থাকতে হয়)
st.set_page_config(page_title="Aryan Bot VIP", layout="wide")

# ২. ডিজাইন কাস্টমাইজেশন (CSS) - লুক সুন্দর করার জন্য
st.markdown("""
    <style>
    .stApp { background-color: #0b141d; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .main { color: white; }
    .stButton>button {
        width: 100%;
        background-color: #23313d;
        color: white !important;
        border: 1px solid #00b977;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
    }
    .stButton>button:hover {
        background-color: #00b977;
        color: black !important;
    }
    .signal-card {
        background-color: #16232d;
        padding: 25px;
        border-radius: 15px;
        border-bottom: 5px solid #00b977;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. লগইন সেশন ম্যানেজমেন্ট
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ৪. লগইন ইন্টারফেস
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00b977;'>ARYAN BOT VIP LOGIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        pw = st.text_input("পাসওয়ার্ড দিন", type="password")
        if st.button("প্রবেশ করুন"):
            if pw == "2023":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("ভুল পাসওয়ার্ড! আবার সঠিক পাসওয়ার্ড দিন।")
else:
    # ৫. মূল ড্যাশবোর্ড (লগইন করার পর)
    st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #00b977; margin:0;'>ARYAN VIP AI SIGNAL</h1>", unsafe_allow_html=True)
    
    # মার্কেট বাটনসমূহ
    markets = ["USD/PKR", "USD/MXN", "USD/BRL", "GBP/USD", "EUR/USD", "USD/DZD"]
    cols = st.columns(3)
    
    for i, m in enumerate(markets):
        with cols[i % 3]:
            if st.button(m):
                st.session_state.current_m = m
                st.session_state.analyzing = True

    # সিগন্যাল এনালাইসিস অংশ
    if 'current_m' in st.session_state:
        st.markdown(f"### মার্কেট: <span style='color:#00b977;'>{st.session_state.current_m}</span>", unsafe_allow_html=True)
        
        if st.session_state.get('analyzing', False):
            with st.spinner('AI এনালাইসিস চলছে...'):
                time.sleep(2) # ২ সেকেন্ড লোডিং
                res = random.choice(["UP 🟢", "DOWN 🔴", "WAIT ⚪"])
                st.session_state.last_res = res
                st.session_state.analyzing = False
        
        if 'last_res' in st.session_state:
            # সিগন্যাল অনুযায়ী কালার কোড
            s_color = "#00ff88" if "UP" in st.session_state.last_res else "#ff4a4a" if "DOWN" in st.session_state.last_res else "#ffffff"
            st.markdown(f"<h1 style='font-size: 60px; color: {s_color};'>{st.session_state.last_res}</h1>", unsafe_allow_html=True)
            st.write("এনালাইসিস সফল হয়েছে।")

    st.markdown("</div>", unsafe_allow_html=True)

    # ৬. কোটেক্স চার্ট (নিচে লাইভ দেখাবে)
    st.markdown("### 📊 Live Trading Chart")
    components.iframe("https://qxbroker.com/en/trade", height=800, scrolling=True)
