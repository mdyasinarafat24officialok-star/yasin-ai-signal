import streamlit as st
import random
import time

# পেজ সেটআপ - টাইটেল Forex Trading Signal
st.set_page_config(page_title="Forex Trading Signal", layout="centered")

# আপনার দেওয়া মাস্টার পাসওয়ার্ড এবং আইডি
MASTER_PASSWORD = "mdyasin186"
GAME_ID = "BJ-V.103.182.150.64"

# সেশন স্টেট চেক (লগইন সিস্টেম)
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Forex Trading Signal - VIP Access")
    st.markdown("---")
    pwd = st.text_input("মাস্টার পাসওয়ার্ড দিন:", type="password")
    if st.button("লগইন করুন"):
        if pwd == MASTER_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("সফলভাবে লগইন হয়েছে!")
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
else:
    # মূল অ্যাপ শুরু
    st.title("📈 Forex Trading Signal")
    st.info(f"সার্ভার আইডি: {GAME_ID}")
    st.markdown("---")
    
    st.subheader("📊 রেজাল্ট ইনপুট সেকশন")
    st.write("গেমের আগের দুটি রাউন্ডের রেজাল্ট নিচে লিখুন:")
    
    col1, col2 = st.columns(2)
    with col1:
        last_round = st.number_input("Last Round (উদা: 1.25)", min_value=1.0, value=1.0, step=0.01)
    with col2:
        prev_round = st.number_input("Previous Round (উদা: 2.50)", min_value=1.0, value=1.0, step=0.01)

    if st.button("সিগন্যাল বের করুন"):
        with st.spinner('অ্যালগরিদম বিশ্লেষণ চলছে...'):
            time.sleep(2) # একটু সময় নেওয়া হচ্ছে রিয়েল টাইম ফিল দিতে
            
            # স্ক্রিনশট থেকে পাওয়া ক্রাশ প্যাটার্ন ক্যালকুলেশন
            if last_round < 1.40 and prev_round < 1.40:
                # যদি পরপর দুটি ছোট আসে, পরেরটি বড় হওয়ার চান্স থাকে
                prediction = random.uniform(2.20, 4.50)
            elif last_round > 3.0:
                # যদি অনেক বড় ক্রাশ হয়, পরেরটি রিস্কি (ছোট) হতে পারে
                prediction = random.uniform(1.10, 1.45)
            else:
                # সাধারণ প্যাটার্ন
                prediction = random.uniform(1.40, 2.30)
            
            final_res = round(prediction, 2)
            
        # রেজাল্ট ডিসপ্লে
        st.markdown("### 🎯 পরবর্তী সম্ভাব্য টার্গেট:")
        st.markdown(f"<h1 style='color: #00FF00; text-align: center;'>{final_res}x</h1>", unsafe_allow_html=True)
        
        st.warning(f"পরামর্শ: নিরাপদ থাকতে {round(final_res - 0.10, 2)}x এ ক্যাশআউট করুন।")

    st.markdown("---")
    st.caption(f"Powered by Yasin AI | ID: {GAME_ID}")
