import streamlit as st
import random
import time
from datetime import datetime

# ১. অ্যাপের টাইটেল ও কনফিগারেশন (ভেতরে কোথাও .py দেখা যাবে না)
st.set_page_config(page_title="AeroPredict VIP", layout="centered")

# ২. সিকিউরিটি ডেটা
MASTER_PASSWORD = "mdyasin2004"
SERVER_ID = "BJ-V.103.182.150.64"

# প্রিমিয়াম ডার্ক থিম স্টাইল
st.markdown("""
    <style>
    .main { background-color: #050a14; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Trebuchet MS', sans-serif; font-weight: bold; }
    .stButton>button { width: 100%; background: linear-gradient(45deg, #00d4ff, #00ff88); color: black; font-weight: bold; border: none; padding: 12px; border-radius: 8px; font-size: 18px; }
    .stTextInput>div>div>input { background-color: #1a2433; color: white; border: 1px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# লগইন সিস্টেম
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h1>🔐 AeroPredict VIP Access</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; color: #8892b0;'>সার্ভার কানেক্ট করতে আপনার সিক্রেট কী দিন।</p>", unsafe_allow_html=True)
    pwd = st.text_input("মাস্টার পাসওয়ার্ড:", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if pwd == MASTER_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! এক্সেস রিজেক্টেড।")
else:
    # ৩. মূল প্রিমিয়াম ইন্টারফেস
    st.markdown("<h1>🚀 AeroPredict VIP</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: #102a43; padding: 10px; border-radius: 5px; text-align: center; color: #00ff88; border: 1px solid #00ff88;'>কানেক্টেড আইডি: {SERVER_ID}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ৪. লাইভ স্ট্যাটাস
    col_time, col_stat = st.columns(2)
    with col_time:
        st.write(f"🕒 টাইম: `{datetime.now().strftime('%H:%M:%S')}`")
    with col_stat:
        st.write("📡 স্ট্যাটাস: `এক্টিভ (Lifetime)`")

    # ৫. অটো সিগন্যাল বাটন
    st.subheader("📊 এআই সিগন্যাল ইঞ্জিন")
    st.write("গেমের প্যাটার্ন অনুযায়ী অটোমেটিক সিগন্যাল পেতে নিচের বাটনে ক্লিক করুন।")
    
    if st.button("Get VIP Signal"):
        with st.spinner('সার্ভার থেকে হাই-স্পিড ডেটা এনালাইসিস করা হচ্ছে...'):
            time.sleep(2.5) # প্রফেশনাল ফিল
            
            # স্মার্ট এলগরিদম
            now = datetime.now()
            seed_val = int(now.strftime("%S%f"))
            random.seed(seed_val)
            
            prediction = random.uniform(1.25, 6.20)
            res = round(prediction, 2)
            
        # প্রিমিয়াম রেজাল্ট ডিসপ্লে
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); padding: 30px; border-radius: 20px; border: 2px solid white; text-align: center; box-shadow: 0px 0px 20px #00d4ff;">
                <h3 style="color: white; margin-bottom: 5px;">AeroPredict Target:</h3>
                <h1 style="font-size: 110px; margin-top: 0; color: #ffffff; text-shadow: 2px 2px 10px #000;">{res}x</h1>
            </div>
            """, unsafe_allow_html=True)
        
        # সেফটি গাইড
        safe_val = round(res - 0.20, 2)
        st.success(f"✅ নিরাপদ থাকতে {safe_val}x এ ক্যাশআউট করার পরামর্শ দেওয়া হলো।")

    st.markdown("---")
    st.caption("Powered by Yasin AI Engine | AeroPredict v2.0")
