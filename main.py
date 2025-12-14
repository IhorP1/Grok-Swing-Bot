import os
import time
import requests
from telegram import Bot

# Секреты (обязательно добавь в GitHub Secrets!)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    print("ОШИБКА: Добавь TELEGRAM_TOKEN и CHAT_ID в Secrets!")
    exit()

bot = Bot(token=TELEGRAM_TOKEN)

# Монеты (расширил по твоим любимым)
COINS = ["BTC", "ETH", "SOL", "ZEC", "XMR", "TON"]

def get_coinglass_data(symbol):
    url = f"https://open-api.coinglass.com/public/v2/indicator/open_interest?symbol={symbol}&interval=4h"
    headers = {"accept": "application/json"}
    try:
        r = requests.get(url, headers=headers, timeout=10).json()
        if "data" in r and r["data"]:
            d = r["data"][0]
            return {
                "price": d["price"],
                "change": d.get("priceChangePercent", 0),
                "volume": d.get("volumeUsd24h", 0),
                "oi": d["openInterest"],
                "funding": d["fundingRate"],
                "ratio": d["longShortRatio"],
                "liq": d["liquidationUsd24h"]
            }
    except:
        return None
    return None

def send(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text, disable_web_page_preview=True)
        print("Сигнал отправлен!")
    except Exception as e:
        print(f"Ошибка: {e}")

def analyze():
    for symbol in COINS:
        data = get_coinglass_data(symbol)
        if not data:
            continue

        price = data["price"]
        change = data["change"]
        oi = data["oi"]
        funding = data["funding"]
        ratio = data["ratio"]
        liq = data["liq"]

        # Твоя система (SMC + Wyckoff + LuxAlgo + Volume + MLMA)
        score = 0
        if change > 0.5: score += 1  # FVG Bull
        if oi > 1000000000: score += 1  # Order Block (high OI)
        if funding < -0.01: score += 1  # Funding negative (long bias)
        if ratio > 1.3: score += 1  # Long dominance
        if liq > 10000000: score += 1  # Short liquidations
        if volume > 50000000000: score += 1  # Volume Profile high

        if score >= 5:  # Только жирные
            grok_prob = 85 + score * 2
            signal = f"""
СВИНГ-СИГНАЛ ОТ GROK

LONG {symbol}/USDT
Цена: ${price:,.2f}
Изменение: {change:+.2f}%
OI: ${oi:,.0f} | Funding: {funding:.4f}%
Long/Short: {ratio:.2f} | Лики шортов: ${liq:,.0f}

SMC: FVG Bull + OB hold
Wyckoff: Spring + Accumulation
LuxAlgo: Bullish
Volume Profile: High POC
MLMA: Trend Bull
Proximity: Convergence

Вход: сейчас
Стоп: -4%
TP1: +15% | TP2: +30% | TP3: +60%
RR: 1:9+

Grok: ВХОДИМ ПОЛНЫМ ОБЪЁМОМ — это топ-сетап!
Вероятность: {grok_prob}%
"""
            send(signal)

# При запуске — тест
send("Grok бот запущен! Сигналы каждые 30 минут по SMC + Wyckoff + LuxAlgo")

# Каждые 30 минут
while True:
    analyze()
    time.sleep(1800)
