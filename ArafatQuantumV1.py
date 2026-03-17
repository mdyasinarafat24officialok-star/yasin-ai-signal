import streamlit as st
import ccxt
import pandas as pd
import pandas_ta as ta
import datetime
import pytz
import time

# পেজ কনফিগারেশন
st.set_page_config(page_title="ARAFAT QUANTUM V1", layout="wide")

# ইউনিক ডেঞ্জারাস ডিজাইন (CSS)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stSelectbox, .stSlider { background-color: #111; border: 1px solid #ff4b4b; border-radius: 10px; color: white; }
    .signal-card { padding: 50px; border-radius: 25px; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; transition: 0.5s; border: 2px solid #333; }
    .timer-box { font-size: 28px; color: #f9d423; text-align: center; font-weight: bold; background: #1a1a1a; padding: 10px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #444; }
    .stButton>button { background: linear-gradient(45deg, #ff4b4b, #8b0000); color: white; font-weight: bold; width: 100%; border-radius: 12px; height: 3.5em; border: none; }
    .stButton>button:hover { background: #ff0000; box-shadow: 0px 0px 15px #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# ১. মাস্টার লগইন সিস্টেম
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; font-size: 45px;'>🛑 ARAFAT QUANTUM V1</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>PREMIUM ALGORITHMIC TRADING INTERFACE</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div style='max-width: 400px; margin: auto; padding: 30px; background: #111; border-radius: 20px; border: 1px solid #ff4b4b;'>", unsafe_allow_html=True)
        user_id = st.text_input("Username", placeholder="Enter ID")
        pass_input = st.text_input("Master Access Code", type="password", placeholder="••••••••")
        
        if st.button("➔ UNLOCK SYSTEM"):
            if pass_input == "Arafat@Vip#Quantum2026":
                st.session_state.authenticated = True
                st.success("Access Granted! Loading Quantum Logic...")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error("Invalid Code! Access Denied.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ২. সাইডবার সেটিংস
st.sidebar.markdown("<h2 style='color: #ff4b4b;'>💎 VIP CONTROL</h2>", unsafe_allow_html=True)
tf_choice = st.sidebar.slider("⏱️ ক্যান্ডেল টাইমফ্রেম (মিনিট)", 1, 30, 1)

# ২৫টি প্রফেশনাল মার্কেট লোগোসহ
markets = {
    "🇪🇺 EUR/USD": "EUR/USD", "🇬🇧 GBP/USD": "GBP/USD", "🇯🇵 USD/JPY": "USD/JPY",
    "🇦🇺 AUD/USD": "AUD/USD", "🇨🇦 USD/CAD": "USD/CAD", "🇨🇭 USD/CHF": "USD/CHF",
    "🇳🇿 NZD/USD": "NZD/USD", "🇪🇺 EUR/GBP": "EUR/GBP", "🇪🇺 EUR/JPY": "EUR/JPY",
    "🇬🇧 GBP/JPY": "GBP/JPY", "🇦🇺 AUD/JPY": "AUD/JPY", "🇪🇺 EUR/AUD": "EUR/AUD",
    "🇪🇺 EUR/CAD": "EUR/CAD", "🇬🇧 GBP/AUD": "GBP/AUD", "🇬🇧 GBP/CAD": "GBP/CAD",
    "🇦🇺 AUD/CAD": "AUD/CAD", "🇨🇦 USD/NOK": "USD/NOK", "🇨🇦 USD/SEK": "USD/SEK",
    "📀 GOLD (XAU/USD)": "XAU/USD", "🥈 SILVER (XAG/USD)": "XAG/USD",
    "🛢️ CRUDE OIL": "USO/USD", "₿ BTC/USDT": "BTC/USDT", "💎 ETH/USDT": "ETH/USDT",
    "🚀 SOL/USDT": "SOL/USDT", "🐕 DOGE/USDT": "DOGE/USDT"
}
selected_label = st.sidebar.selectbox("🌐 মার্কেট নির্বাচন করুন", list(markets.keys()))
selected_symbol = markets[selected_label]

# ৩. লাইভ ডেটা ও এনালাইসিস ফাংশন
def get_analysis(symbol, tf):
    try:
        ex = ccxt.binance()
        # গোল্ড বা অন্য সিম্বল অ্যাডজাস্টমেন্ট
        symbol_map = {"XAU/USD": "PAXG/USDT", "XAG/USD": "XAG/USDT"}
        trade_symbol = symbol_map.get(symbol, symbol)
        
        bars = ex.fetch_ohlcv(trade_symbol, timeframe=f'{tf}m', limit=50)
        df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
        
        rsi = ta.rsi(df['c'], length=14).iloc[-1]
        bb = ta.bbands(df['c'], length=20, std=2)
        price = df['c'].iloc[-1]
        lower_bb = bb['BBL_20_2.0'].iloc[-1]
        upper_bb = bb['BBU_20_2.0'].iloc[-1]
        
        return price, rsi, lower_bb, upper_bb
    except:
        return None, None, None, None

# ৪. মেইন ড্যাশবোর্ড
st.markdown(f"<h2 style='text-align: center; color: #ff4b4b;'>🚀 {selected_label} - QUANTUM ANALYSIS</h2>", unsafe_allow_html=True)

# ক্যান্ডেল টাইমার হিসেব (বাংলাদেশ সময়)
tz_bd = pytz.timezone('Asia/Dhaka')
now = datetime.datetime.now(tz_bd)
seconds_passed = (now.minute % tf_choice) * 60 + now.second
seconds_remaining = (tf_choice * 60) - seconds_passed

st.markdown(f"<div class='timer-box'>পরবর্তী ক্যান্ডেল শুরু হতে বাকি: {seconds_remaining} সেকেন্ড</div>", unsafe_allow_html=True)

# সিগন্যাল জেনারেশন
price, rsi, low, high = get_analysis(selected_symbol, tf_choice)

if price:
    sig_text = "ANALYZING... 🛰️"
    sig_color = "#1a1a1a"
    reason = "সঠিক কনফার্মেশনের জন্য অপেক্ষা করছি..."

    # ৪০-৪৫ সেকেন্ড আগে সিগন্যাল ডিটেক্ট করবে
    if rsi < 32 and price <= low:
        sig_text = "CALL (UP) ⬆️"
        sig_color = "#00ffcc"
        reason = "স্ট্রং সাপোর্ট জোন! পরবর্তী ক্যান্ডেল উপরে যাবে।"
    elif rsi > 68 and price >= high:
        sig_text = "PUT (DOWN) ⬇️"
        sig_color = "#ff4b4b"
        reason = "রেজিস্ট্যান্স জোন! পরবর্তী ক্যান্ডেল নিচে যাবে।"
    
    # শেষ ৫ সেকেন্ডের ডেঞ্জার চেক
    if seconds_remaining <= 5:
        if (sig_text != "ANALYZING... 🛰️") and (rsi > 45 and rsi < 55):
            sig_text = "⚠️ RISK - DO NOT ENTER"
            sig_color = "#f9d423"
            reason = "মার্কেট ভলিউম কম, এই ক্যান্ডেল এড়িয়ে চলুন!"

    st.markdown(f"""
        <div class="signal-card" style="background-color: {sig_color}; box-shadow: 0px 0px 20px {sig_color};">
            <h1 style="font-size: 70px; margin: 0; color: white;">{sig_text}</h1>
            <p style="font-size: 20px; color: white; opacity: 0.9;">{reason}</p>
        </div>
    """, unsafe_allow_html=True)

# ৫. স্ট্যাটিস্টিকস ও বাটন
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.button("✅ WIN / SURE SHOT")
with c2: st.button("❌ LOSS / RECOVERY")
with c3: st.button("🔄 MANUAL REFRESH")

# অটো রিফ্রেশ লজিক
time.sleep(5)
st.rerun()
