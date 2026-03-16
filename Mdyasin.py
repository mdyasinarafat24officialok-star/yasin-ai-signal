import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime
import time

# ১. প্রাথমিক সেটআপ ও স্টাইল
st.set_page_config(page_title="Yasin AI Pro Signal", page_icon="📈", layout="wide")

# কাস্টম সিএসএস স্টাইল
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .signal-box { padding: 40px; border-radius: 20px; text-align: center; border: 2px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# ২. পাসওয়ার্ড সিকিউরিটি (আপনার দেওয়া ৬ সংখ্যার কোড)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Yasin AI Access Control")
    password = st.text_input("৬ সংখ্যার সিক্রেট পাসওয়ার্ড দিন:", type="password")
    if st.button("লগইন করুন"):
        if password == "123456":  # এখানে আপনার পাসওয়ার্ড (১২৩৪৫৬) দেওয়া আছে
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
    st.stop()

# ৩. সিগন্যাল ড্যাশবোর্ড (লগইন হওয়ার পর)
st.title("🚀 Yasin AI - Real-Time Smart Signal")
st.sidebar.header("⚙️ কন্ট্রোল প্যানেল")

# কারেন্সি লিস্ট সাথে লোগো (ইমোজি ব্যবহার করা হয়েছে সুন্দর দেখানোর জন্য)
market_map = {
    "🇵🇰 USD/PKR": "USDPKR=X",
    "🇲🇽 USD/MXN": "USDMXN=X",
    "🇧🇷 USD/BRL": "USDBRL=X",
    "🇳🇿 USD/NZD": "USDNZD=X",
    "🇨🇴 USD/COP": "USDCOP=X",
    "🇦🇷 USD/ARS": "USDARS=X",
    "🇩🇿 USD/DZD": "USDDZD=X"
}

selected_label = st.sidebar.selectbox("মার্কেট সিলেক্ট করুন:", list(market_map.keys()))
symbol = market_map[selected_label]
timeframe = st.sidebar.selectbox("টাইমফ্রেম (এনালাইসিস টাইম):", ["1m", "5m", "15m", "30m", "1h"])

# ৪. সিগন্যাল লজিক (SMC + RSI + Trend)
def calculate_signal(df):
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['EMA_200'] = ta.ema(df['Close'], length=200)
    
    last = df.iloc[-1]
    prev = df.iloc[-2]
    
    # বাই সিগন্যাল: দাম ২০০ ইএমএ-র উপরে এবং আরএসআই নিচে (OverSold)
    if last['Close'] > last['EMA_200'] and last['RSI'] < 35:
        return "🔥 STRONG BUY", "#00FF7F" # স্প্রিং গ্রিন
    # সেল সিগন্যাল: দাম ২০০ ইএমএ-র নিচে এবং আরএসআই উপরে (OverBought)
    elif last['Close'] < last['EMA_200'] and last['RSI'] > 65:
        return "📉 STRONG SELL", "#FF4B4B" # উজ্জ্বল লাল
    else:
        return "⌛ WAIT (No Signal)", "#FFD700" # গোল্ডেন

# ৫. লাইভ মার্কেট ডাটা আপডেট
try:
    with st.spinner('মার্কেট এনালাইসিস করা হচ্ছে...'):
        data = yf.download(symbol, period="2d", interval=timeframe)
        
    if not data.empty:
        decision, color = calculate_signal(data)
        current_price = data.iloc[-1]['Close']

        # বড় সিগন্যাল বক্স
        st.markdown(f"""
            <div class="signal-box" style="background-color: {color}22; border-color: {color};">
                <h3 style="color: {color}; margin: 0;">{selected_label} - {timeframe} এনালাইসিস</h3>
                <h1 style="color: {color}; font-size: 60px; margin: 10px 0;">{decision}</h1>
                <h2 style="color: white;">লাইভ প্রাইস: {current_price:.4f}</h2>
                <p style="color: #888;">আপডেট টাইম: {datetime.now().strftime('%H:%M:%S')}</p>
            </div>
        """, unsafe_allow_html=True)

        # ট্রেডিং চার্ট
        st.subheader("📊 মার্কেট চার্ট")
        st.line_chart(data['Close'])
        
    else:
        st.error("ডাটা পাওয়া যায়নি। মার্কেট এখন বন্ধ থাকতে পারে।")

except Exception as e:
    st.error(f"Error: {e}")

# ৬. অটো রিফ্রেশ (প্রতি ৬০ সেকেন্ডে)
time.sleep(60)
st.rerun()
