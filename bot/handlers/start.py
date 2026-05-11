from telegram import Update
from telegram.ext import ContextTypes

from bot.database.db import SessionLocal
from bot.database.models import User
from bot.keyboards.keyboards import language_keyboard, main_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    tg_id = update.effective_user.id

    async with SessionLocal() as session:

        user = await session.get(User, tg_id)

        if not user:
            await update.message.reply_text(
                "Выберите язык:",
                reply_markup=language_keyboard()
            )
            return

    await update.message.reply_text(
        "Бот готов к работе ✅",
        reply_markup=main_keyboard()
    )
