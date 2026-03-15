import streamlit as st
import numpy as np
from datetime import datetime
import time

# ১. হাই-প্রোফাইল অ্যাপ সেটআপ
st.set_page_config(page_title="ULTIMATE AI MASTER - YASIN", layout="wide")

# সিউশন স্টেট চেক
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ২. নতুন পাসওয়ার্ড সিস্টেম (mdyasin186)
if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🛡️ VIP MASTER AI ACCESS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("সিক্রেট মাস্টার পাসওয়ার্ড দিন:", type="password")
