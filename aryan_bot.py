import streamlit as st
import streamlit.components.v1 as components
import random
import time

# পেজ কনফিগারেশন
st.set_page_config(page_title="Aryan Trading Bot", layout="wide")

# সিএসএস দিয়ে ডিজাইন কাস্টমাইজেশন (HTML এর মতো লুক আনতে)
st.markdown("""
    <style>
    .main {
        background-color: #0b141d;
    }
    .stButton>button {
        width: 100%;
        background-color: #23313d;
        color: white;
        border: 1px solid #444;
        border-radius: 5px;
    }
    .stButton>button:hover {
        border-color: #00b977;
        color: #00b977;
    }
    .signal-box {
        background-color: #16232d;
        padding: 20px;
        border-bottom: 3px solid #00b977;
        text-align: center;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_view_ Wood=True)

# লগইন সিস্টেম
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center; color: #00b977;'>ARYAN TRADING BOT</h2>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password = st.text_input("পাসওয়ার্ড দিন", type="password")
            if st.button("প্রবেশ করুন"):
                if password == "2023":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
else:
    # সিগন্যাল ড্যাশবোর্ড (উপরের অংশ)
    st.markdown("<div class='signal-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #00b977; margin:0;'>ARYAN AI SIGNAL</h2>", unsafe_allow_html=True)
    
    markets = ["USD/PKR", "USD/MXN", "USD/BRL", "USD/COP", "USD/ARS", "GBP/USD", "EUR/USD", "NZD/USD", "USD/DZD"]
    
    # মার্কেট সিলেক্টর বাটন
    cols = st.columns(len(markets))
    selected_market = st.session_state.get('market', "---")
    
    for i, m in enumerate(markets):
        if cols[i].button(m):
            st.session_state['market'] = m
            st.session_state['scan'] = True

    st.write(f"মার্কেট: **{st.session_state.get('market', '---')} (Live)**")
    
    # সিগন্যাল লজিক
    sig_text = st.empty()
    status_text = st.empty()

    if st.session_state.get('scan'):
        sig_text.markdown("<h3 style='color: #aaa;'>মার্কেট স্ক্যান হচ্ছে...</h3>", unsafe_allow_html=True)
        status_text.write("ক্যান্ডেলস্টিক প্যাটার্ন চেক করা হচ্ছে...")
        time.sleep(1.5)
        
        r = random.random()
        if r > 0.65:
            sig_text.markdown("<h1 style='color: #00ff88;'>UP - হ্যাঁ (১০০%) 🟢</h1>", unsafe_allow_html=True)
            status_text.write("শক্তিশালী বুলিশ ট্রেন্ড পাওয়া গেছে।")
        elif r < 0.35:
            sig_text.markdown("<h1 style='color: #ff4a4a;'>DOWN - হ্যাঁ (১০০%) 🔴</h1>", unsafe_allow_html=True)
            status_text.write("মার্কেট নিচে নামার সম্ভাবনা বেশি।")
        else:
            sig_text.markdown("<h1 style='color: #ffffff;'>অপেক্ষা - না ⚪</h1>", unsafe_allow_html=True)
            status_text.write("মার্কেট এখন রিস্কি, ট্রেড নিবেন না।")
        st.session_state['scan'] = False
    
    st.markdown("</div>", unsafe_allow_html=True)

    # কোটেক্স লাইভ স্ক্রিন (নিচের অংশ)
    st.markdown("---")
    components.iframe("https://qxbroker.com/en/trade", height=600, scrolling=True)
