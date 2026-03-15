import streamlit as st
import random
import time
from datetime import datetime

# পেজ কনফিগারেশন
st.set_page_config(page_title="AeroPredict VIP", layout="centered")

# পাসওয়ার্ড ও আইডি
MASTER_PASSWORD = "mdyasin2004"
SERVER_ID = "BJ-V.103.182.150.64"

# মোবাইল ফ্রেন্ডলি ডিজাইন
st.markdown("""
    <style>
    .main { background-color: #050a14; }
    .stButton>button { 
        height: 150px; 
        font-size: 25px; 
        background: linear-gradient(45deg, #ff0055, #00d4ff); 
        color: white; 
        border-radius: 20px;
        font-weight: bold;
    }
    h1 { color: #00ff88; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 VIP LOGIN")
    pwd = st.text_input("পাসওয়ার্ড:", type="password")
    if st.button("UNLOCK"):
        if pwd == MASTER_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
else:
    st.markdown("<h1>🚀 AeroPredict VIP</h1>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center; color: gray;'>ID: {SERVER_ID}</p>", unsafe_allow_html=True)

    # বড় বাটন যাতে ৫ সেকেন্ডের মধ্যে চাপ দেওয়া যায়
    st.subheader("ক্লিক করুন (টাইপ করার দরকার নেই)")
    
    if st.button("🔥 GET NEXT SIGNAL"):
        with st.spinner('⚡'):
            # দ্রুত ক্যালকুলেশন লজিক
            time.sleep(0.5) # ১ সেকেন্ডেরও কম সময় নেবে
            
            now = datetime.now()
            # সময়ের সেকেন্ড ব্যবহার করে অটো প্যাটার্ন তৈরি
            sec = now.second
            
            if sec % 3 == 0:
                res = round(random.uniform(1.10, 1.50), 2) # সেফ মোড
            elif sec % 5 == 0:
                res = round(random.uniform(2.00, 3.50), 2) # মিডিয়াম
            else:
                res = round(random.uniform(1.50, 2.20), 2) # স্ট্যাবল
                
        # বড় এবং উজ্জ্বল রেজাল্ট প্রদর্শন
        st.markdown(f"""
            <div style="background: black; padding: 20px; border-radius: 15px; border: 5px solid #00ff88; text-align: center;">
                <h1 style="font-size: 80px; color: #00ff88; margin: 0;">{res}x</h1>
            </div>
            """, unsafe_allow_html=True)
        
        st.write(f"<p style='text-align: center; color: yellow;'>সময়: {now.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Auto-Sync Active | Manual Typing Disabled")
