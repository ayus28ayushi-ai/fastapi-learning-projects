import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CURRENCY_EXCHANGE_API_KEY = os.getenv("CURRENCY_EXCHANGE_API_KEY")