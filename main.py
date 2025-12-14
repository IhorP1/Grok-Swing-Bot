import os
import time
import requests
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    print("ОШИБКА: Добавь секреты в GitHub!")
    exit()

bot = Bot(token=TELEGRAM_TOKEN)

def send(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text, disable_web_page_preview=True)
        print("Уровни отправлены!")
    except Exception as e:
        print(f"Ошибка: {e}")

def get_levels():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
        data = requests.get(url).json()["bitcoin"]
        price = data["usd"]
        change = data["usd_24h_change"]
        volume = data["usd_24h_vol"]

        support = round(price * 0.97)
        resistance = round(price * 1.06)
        poc = round(price)
        fvg = f"{round(price * 0.985)} — {round(price * 1.015)}"

        signal = f"""
УРОВНИ BTC — ОБНОВЛЕНО

Цена: ${price:,.0f}
Изменение 24ч: {change:+.2f}%
Объём: ${volume:,.1f}B

• Поддержка: ${support:,.0f}
• Сопротивление: ${resistance:,.0f}
• POC: ${poc:,.0f}
• FVG зона: {fvg}$

Grok: {'LONG bias — ждём отскок' if change > -1 else 'Осторожно — возможен пробой вниз'}
Следующее обновление через 1 час
"""
        send(signal)
    except Exception as e:
        send(f"Ошибка данных: {e}")

# Сразу при запуске — первый сигнал
get_levels()

# Больше ничего — GitHub сам перезапустит через час
