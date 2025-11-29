"""
Webhook TradingView → Telegram
Fichier: webhook_telegram.py
"""

from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Configuration (utiliser variables d'environnement en production)
TELEGRAM_TOKEN = os.getenv("8033410847:AAGwntCkMJtD85enDHc16YFAEPV-La2djYI", "8033410847:AAGwntCkMJtD85enDHc16YFAEPV-La2djYI")
TELEGRAM_CHAT_ID = os.getenv("testbot1510", "testbot1510")

def send_telegram(message: str) -> bool:
    """Envoie un message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"Erreur Telegram: {e}")
        return False

@app.route("/webhook", methods=["POST"])
def webhook():
    """Reçoit les alertes TradingView et les forward à Telegram."""
    data = request.get_data(as_text=True)
    
    if not data:
        return "No data", 400
    
    # TradingView envoie le message brut dans le body
    send_telegram(f"🚨 <b>Alerte TradingView</b>\n\n{data}")
    
    return "OK", 200

@app.route("/", methods=["GET"])
def health():
    return "Webhook actif", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
