import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID larni xatosiz xavfsiz o'qib olish
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID", 0))

DATABASE_URL = os.getenv("DATABASE_URL")
