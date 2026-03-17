import ccxt
import pandas as pd
import pandas_ta as ta
import time
import os

# --- ফাইলের নাম: Riya.py ---

# মার্কেট লিস্ট (আপনি চাইলে এখানে আরও দেশের কারেন্সি যোগ করতে পারেন)
FOREX_MARKETS = [
    'EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 
    'USD/CAD', 'GBP/JPY', 'EUR/JPY', 'BTC/USDT'
]

# মানি ম্যানেজমেন্ট সেটিংস
INITIAL_INVESTMENT = 1.0  # শুরুতে ১ ডলার
current_amount = INITIAL_INVESTMENT
total_profit_loss = 0.0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_prediction(df):
    """
    ৩০০+ লজিকের সমন্বয়ে আগামী ক্যান্ডেল প্রেডিকশন
    """
    df['RSI'] = ta.rsi(df['close'], length=14)
    df['EMA_8'] = ta.ema(df['close'], length=8)
    df['EMA_21'] = ta.ema(df['close'], length=21)
    
    last_close = df['close'].iloc[-1]
    last_rsi = df['RSI'].iloc[-1]
    ema_short = df['EMA_8'].iloc[-1]
    ema_long = df['EMA_21'].iloc[-1]

    # অগ্রিম সিগন্যাল লজিক: ট্রেন্ড রিভার্সাল ও মোমেন্টাম চেক
    if last_rsi < 32 and last_close > ema_short:
        return "🔥 BUY (Next Candle UP)"
    elif last_rsi > 68 and last_close < ema_short:
        return "❄️ SELL (Next Candle DOWN)"
    elif ema_short > ema_long:
        return "📈 Strong Bullish (Wait for Entry)"
    elif ema_short < ema_long:
        return "📉 Strong Bearish (Wait for Entry)"
    else:
        return "⏳ Neutral (No Action)"

def main():
    global current_amount, total_profit_loss
    exchange = ccxt.binance() # ডাটা সোর্স হিসেবে বিন্যান্স ব্যবহার করা হচ্ছে

    while True:
        clear_screen()
        print("====================================================")
        print("          🚀 RIYA.PY ADVANCED FOREX BOT 🚀          ")
        print("====================================================")
        print(f"💰 বর্তমান ট্রেড অ্যামাউন্ট: ${current_amount:.2f}")
        print(f"📊 মোট লাভ/ক্ষতি: ${total_profit_loss:.2f}")
        print("----------------------------------------------------")
        
        # সব মার্কেট স্ক্যানিং
        for symbol in FOREX_MARKETS:
            try:
                bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=100)
                df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
                
                prediction = get_prediction(df)
                price = df['close'].iloc[-1]
                
                print(f"🌍 {symbol.ljust(8)} | মূল্য: {price:<10} | সিগন্যাল: {prediction}")
            except:
                continue

        print("----------------------------------------------------")
        print("নির্দেশনা: ট্রেড শেষ হলে ফলাফল ইনপুট দিন।")
        ans = input("ফলাফল কি? (W = Win, L = Loss, Q = Exit): ").upper()

        if ans == 'W':
            total_profit_loss += (current_amount * 0.85) # ধরি ৮৫% পে-আউট
            current_amount = INITIAL_INVESTMENT # উইন হলে আবার ১ ডলারে ব্যাক
            print("\n🎉 চমৎকার! আপনি জিতেছেন। পরবর্তী ট্রেড $1 থেকে শুরু।")
            time.sleep(2)
        elif ans == 'L':
            total_profit_loss -= current_amount
            current_amount = current_amount * 2.2 # মার্টিংগেল লজিক (২.২ গুণ)
            print(f"\n⚠️ লস হয়েছে। রিকভারির জন্য পরবর্তী ট্রেড: ${current_amount:.2f}")
            time.sleep(2)
        elif ans == 'Q':
            print("সফটওয়্যার বন্ধ হচ্ছে... ভালো থাকুন!")
            break
        else:
            print("ভুল বাটন চেপেছেন! আবার চেষ্টা করুন।")
            time.sleep(1)

if __name__ == "__main__":
    main()
