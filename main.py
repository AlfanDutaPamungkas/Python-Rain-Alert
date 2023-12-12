import os
import requests
import smtplib
from dotenv import load_dotenv

load_dotenv()

LATITUDE  = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")
APP_ID = os.getenv("APP_ID")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TARGET_EMAIL = os.getenv("TARGET_EMAIL")

param = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": APP_ID,
    "exclude":"current,minutely,daily"
}

response = requests.get(url="https://api.openweathermap.org/data/2.8/onecall", params=param)
response.raise_for_status()
weather_data = response.json()

hour = weather_data["hourly"][:12]
weather_id = [i["weather"][0]["id"] for i in hour]

for id in weather_id:
    if id < 700:
        message_mail = "It's going to rain today. Remember to bring an umbrella"
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=TARGET_EMAIL,
                msg=f"Subject:Rain Alert\n\n{message_mail}"
            )
        break
