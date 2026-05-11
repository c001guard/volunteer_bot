import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_CREDS = os.getenv("GOOGLE_CREDS")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

if not all([BOT_TOKEN, DATABASE_URL, GOOGLE_CREDS, SPREADSHEET_ID]):
    raise RuntimeError("ENV variables missing")
