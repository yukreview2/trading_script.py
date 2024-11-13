# trading_script.py

from pycoingecko import CoinGeckoAPI
import pandas as pd
import talib
from telegram import Bot
import schedule
import time

# Initialize API and Telegram Bot
cg = CoinGeckoAPI()
TELEGRAM_TOKEN = '7652372718:AAGJy92PsoSyOvh8p5tDoOzKtnd0ShuIj3g'
CHAT_ID = '5523100058'
bot = Bot(token=bot_token)

# Define the analysis function
def analyze_token():
    data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days='1')
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['SMA'] = talib.SMA(df['price'], timeperiod=14)
    df['RSI'] = talib.RSI(df['price'], timeperiod=14)
    
    # Detect signal condition (example: RSI crossover)
    if df['RSI'].iloc[-1] > 70:
        bot.send_message(chat_id=chat_id, text="RSI is over 70, consider selling.")
    elif df['RSI'].iloc[-1] < 30:
        bot.send_message(chat_id=chat_id, text="RSI is below 30, consider buying.")

# Schedule the job every hour
schedule.every(1).hour.do(analyze_token)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
