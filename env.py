import os
from dotenv import load_dotenv

load_dotenv()
#Telegram
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHANNEL = os.getenv("CHANNEL")