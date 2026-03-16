import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime
import time

# পেজ সেটআপ ও প্রো-ডিজাইন
st.set_page_config(page_title="Yasin Official AI Bot", page_icon="💹", layout="wide")

# কাস্টম ব্ল্যাক ও গোল্ড থিম ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .signal-box { padding: 40px; border-radius: 25px; text-align: center; border: 4px solid; margin: 10px 0; }
    .price-text { font-size: 24px; font-weight: bold; color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# পিন লক সিস্টেম (আপনার জন্য ৬ সংখ্যার সিক্রেট পিন)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Yasin AI Private Access")
    pin = st.text_input("আপনার ৬ সংখ্যার সিক্রেট পিন দিন:", type="password")
    if st.button("Unlock Dashboard"):
        if pin == "654321": # আপনার বর্তমান পিন
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("ভুল পিন! সঠিক পিন ছাড়া অ্যাপ ব্যবহার করা যাবে না।")
    st.stop()

# ড্যাশবোর্ড কন্টেন্ট
st.title("🚀 Yasin Official AI Smart Trading")

# কারেন্সি লিস্ট সাথে দেশের ফ্ল্যাগ লোগো
markets = {
    "🇵🇰 USD/PKR": "USDPKR=X",
    "🇲🇽 USD/MXN": "USDMXN=X",
    "🇧🇷 USD/BRL": "USDBRL=X",
    "🇳🇿 USD/NZD": "USDNZD=X",
    "🇨🇴 USD/COP": "USDCOP=X",
    "🇦🇷 USD/ARS": "USDARS=X",
    "🇩🇿 USD/DZD": "USDDZD=X"
}

# সাইডবার সেটিংস
selected_label = st.sidebar.selectbox("কারেন্সি সিলেক্ট করুন:", list(markets.keys()))
symbol = markets[selected_label]
tf = st.sidebar.selectbox("টাইমফ্রেম সিলেক্ট করুন:", ["1m", "5m", "15m", "30m", "1h"])

# উন্নত সিগন্যাল লজিক (SMC + RSI + Trend)
def analyze_market(df):
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['EMA_200'] = ta.ema(df['Close'], length=200)
    df['EMA_50'] = ta.ema(df['Close'], length=50)
    
    last = df.iloc[-1]
    
    # বাই সিগন্যাল: ট্রেন্ড পজিটিভ + আরএসআই কম
    if last['Close'] > last['EMA_200'] and last['RSI'] < 38:
        return "🔥 STRONG BUY", "#00FF00" # গ্রিন
    # সেল সিগন্যাল: ট্রেন্ড নেগেটিভ + আরএসআই বেশি
    elif last['Close'] < last['EMA_200'] and last['RSI'] > 62:
        return "📉 STRONG SELL", "#FF0000" # রেড
    else:
        return "⌛ WAITING", "#555555" # গ্রে

# লাইভ মার্কেট ডাটা ফেচিং
try:
    data = yf.download(symbol, period="2d", interval=tf)
    if not data.empty:
        signal, color = analyze_market(data)
        current_price = data['Close'].iloc[-1]

        # বড় সিগন্যাল ডিসপ্লে বক্স
        st.markdown(f"""
            <div class="signal-box" style="border-color: {color}; background-color: {color}11;">
                <h3 style="color: {color};">{selected_label} মার্কেট বর্তমানে:</h3>
                <h1 style="color: {color}; font-size: 80px; margin: 10px 0;">{signal}</h1>
                <p class="price-text">লাইভ প্রাইস: {current_price:.4f}</p>
                <p style="color: #888;">টাইমফ্রেম: {tf} | আপডেট: {datetime.now().strftime('%H:%M:%S')}</p>
            </div>
        """, unsafe_allow_html=True)

        # লাইভ ক্যান্ডেল চার্ট
        st.subheader(f"📊 {selected_label} লাইভ মুভমেন্ট")
        st.line_chart(data['Close'])
        
    else:
        st.warning("মার্কেট ডাটা পাওয়া যাচ্ছে না। কিছুক্ষণ অপেক্ষা করুন।")

except Exception as e:
    st.error(f"Error: {e}")

# প্রতি ৬০ সেকেন্ডে অটো রিফ্রেশ
time.sleep(60)
st.rerun()
