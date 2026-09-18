import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID"))
DATABASE_URL = os.getenv("DATABASE_URL")
