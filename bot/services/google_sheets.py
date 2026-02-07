import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import asyncio

from bot.config import GOOGLE_CREDS, SPREADSHEET_ID


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def sync_append(data):

    creds = Credentials.from_service_account_file(
        GOOGLE_CREDS,
        scopes=scope
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    today = datetime.now().strftime("%Y-%m-%d")

    try:
        sheet = spreadsheet.worksheet(today)

    except:
        sheet = spreadsheet.add_worksheet(
            title=today,
            rows="1000",
            cols="10"
        )

        sheet.append_row([
            "Telegram ID",
            "Nick",
            "Type",
            "Start",
            "End",
            "Hours"
        ])

    sheet.append_row(data)


async def log_shift_to_sheet(**kwargs):

    data = [
        kwargs["tg_id"],
        kwargs["platform_nick"],
        kwargs["location"],
        kwargs["start"].strftime("%H:%M"),
        kwargs["end"].strftime("%H:%M"),
        kwargs["duration"]
    ]

    await asyncio.to_thread(sync_append, data)
