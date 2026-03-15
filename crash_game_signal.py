import streamlit as st
import random
import time
from datetime import datetime

# পেজ কনফিগারেশন - VIP লুক
st.set_page_config(page_title="Crash Game Signal VIP", layout="centered")

# আপনার দেওয়া নির্দিষ্ট তথ্য
MASTER_PASSWORD = "mdyasin2004"
SERVER_ID = "BJ-V.103.182.150.64"

# স্টাইল সেটআপ - সবুজ এবং কালো থিম
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00FF00; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { width: 100%; background-color: #00FF00; color: black; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# লগইন সিস্টেম
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🛡️ Crash Game Signal - VIP Access")
    st.write("সার্ভার আইডি কানেক্ট করতে পাসওয়ার্ড দিন।")
    pwd = st.text_input("মাস্টার পাসওয়ার্ড:", type="password")
    if st.button("Unlock System"):
        if pwd == MASTER_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! ভিআইপি এক্সেস রিজেক্টেড।")
else:
    # মূল ইন্টারফেস
    st.title("🚀 Crash Game Signal VIP")
    st.success(f"সার্ভার কানেক্টেড: {SERVER_ID}")
    
    # রিয়েল টাইম ক্লক
    current_time = datetime.now().strftime
