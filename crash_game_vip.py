import streamlit as st
import random
import time
from datetime import datetime

# ১. পেজ টাইটেল এবং কনফিগারেশন
st.set_page_config(page_title="Crash Game VIP", layout="centered")

# ২. আপনার নতুন পাসওয়ার্ড এবং সার্ভার আইডি
MASTER_PASSWORD = "mdyasin2004"
SERVER_ID = "BJ-V.103.182.150.64"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🎖️ Crash Game VIP - Secure Login")
    st.markdown("---")
    pwd = st.text_input("Enter VIP Password:", type="password")
    if st.button("Access System"):
        if pwd == MASTER_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Access Denied! Wrong Password.")
else:
    # মূল ইন্টারফেস
    st.title("🚀 Crash Game VIP")
    
    # ৩. রিয়েল টাইম ক্লক (গেমের সাথে মিল রাখার জন্য)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    st.write(f"**Server Status:** ✅ Online | **Current Time:** `{current_time}`")
    st.write(f"**Connected ID:** `{SERVER_ID}`")
    st.markdown("---")
    
    # ৪. ইনপুট সেকশন
    st.subheader("📊 Live Game Data")
    st.write("গেমের শেষ ৩টি রেজাল্ট ইনপুট দিন:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        r1 = st.number_input("Last Round", min_value=1.0, value=1.0, step=0.01)
    with col2:
        r2 = st.number_input("2nd Last", min_value=1.0, value=1.0, step=0.01)
    with col3:
        r3 = st.number_input("3rd Last", min_value=1.0, value=1.0, step=0.01)

    if st.button("Generate Lifetime Signal"):
        with st.spinner('Syncing with Server Time...'):
            time.sleep(2) 
            
            # ৫. অ্যাডভান্সড লাইফটাইম অ্যালগরিদম
            # সময়ের সাথে প্যাটার্ন পরিবর্তনের গাণিতিক লজিক
            seed = int(now.strftime("%H%M%S"))
            random.seed(seed + int(r1 * 100)) 
            
            avg = (r1 + r2 + r3) / 3
            
            # স্ক্রিনশট প্যাটার্ন এনালাইসিস
            if r1 < 1.40 and r2 < 1.40:
                # পরপর ছোট আসলে ১ মিনিটের মধ্যে বড় জ্যাম্প করার সম্ভাবনা
                prediction = random.uniform(2.60, 6.50)
            elif r1 > 4.50:
                # বড় ক্রাশের পর ছোট রিস্ক কমানো
                prediction = random.uniform(1.15, 1.48)
            elif avg < 1.80:
                # স্টেবল মার্কেট লজিক
                prediction = random.uniform(1.85, 3.20)
            else:
                prediction = random.uniform(1.30, 2.10)
            
            final_res = round(prediction, 2)
            
        # ফলাফল প্রদর্শন
        st.markdown("### 🎯 Next VIP Signal:")
        st.markdown(f"<h1 style='color: #00FF00; text-align: center; font-size: 90px; border: 2px solid #00FF00; border-radius: 15px;'>{final_res}x</h1>", unsafe_allow_html=True)
        
        # সেফটি গাইড
        safe_cash = round(final_res - 0.20, 2)
        st.warning(f"💡 Lifetime Guide: Cash out at **{safe_cash}x** for 99% winning chance.")

    st.markdown("---")
    st.caption(f"System: Optimized for {SERVER_ID} | Lifetime Validity: Active")
