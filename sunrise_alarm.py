import requests
from datetime import datetime, timedelta
import pytz
import time
import winsound
import os
from plyer import notification
from dotenv import load_dotenv

# ================= LOAD ENV =================
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ================= USER SETTINGS =================
CITY_LAT = 28.644800     # New Delhi
CITY_LON = 77.216721
TIMEZONE = "Asia/Kolkata"
ALERT_BEFORE_MINUTES = 10
# ===============================================

def get_sunrise_time():
    url = f"https://api.sunrise-sunset.org/json?lat={CITY_LAT}&lng={CITY_LON}&formatted=0"
    data = requests.get(url).json()
    return datetime.fromisoformat(data["results"]["sunrise"])

def send_telegram_alert():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "🌅 Sunrise in 10 minutes!"
    }
    requests.post(url, data=payload)

def main():
    tz = pytz.timezone(TIMEZONE)

    sunrise_utc = get_sunrise_time()
    sunrise_local = sunrise_utc.astimezone(tz)
    alert_time = sunrise_local - timedelta(minutes=ALERT_BEFORE_MINUTES)

    print("Sunrise:", sunrise_local)
    print("Alert at:", alert_time)

    while datetime.now(tz) < alert_time:
        time.sleep(30)

    # 🔔 ALARM
    winsound.Beep(1000, 5000)

    # 📢 NOTIFICATION
    notification.notify(
        title="🌅 Sunrise Alert",
        message="Sunrise in 10 minutes",
        timeout=15
    )

    # 📩 TELEGRAM
    send_telegram_alert()

if __name__ == "__main__":
    main()
