from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.database.db import SessionLocal
from bot.database.models import User
from bot.keyboards.keyboards import main_keyboard


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):

    tg_id = update.effective_user.id
    text = update.message.text

    lang = "ru" if text == "Русский" else "uz"

    async with SessionLocal() as session:

        user = await session.get(User, tg_id)

        if not user:
            user = User(
                telegram_id=tg_id,
                platform_nick=str(tg_id),
                language=lang
            )
            session.add(user)
        else:
            user.language = lang

        await session.commit()

    await update.message.reply_text(
        "Язык сохранён ✅",
        reply_markup=ReplyKeyboardRemove()
    )

    await update.message.reply_text(
        "Бот готов к работе 🚀",
        reply_markup=main_keyboard()
    )
