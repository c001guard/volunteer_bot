from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import ContextTypes

from bot.database.db import SessionLocal
from bot.database.models import User, Shift
from bot.services.google_sheets import log_shift_to_sheet
from bot.keyboards.keyboards import shift_keyboard, main_keyboard

TZ = ZoneInfo("Asia/Tashkent")


async def arrived(update: Update, context: ContextTypes.DEFAULT_TYPE):

    tg_id = update.effective_user.id

    async with SessionLocal() as session:

        active_shift = await Shift.get_active_shift(session, tg_id)

        if active_shift:
            await update.message.reply_text(
                "⚠️ У тебя уже есть активная смена.",
                reply_markup=main_keyboard()
            )
            return

    await update.message.reply_text(
        "Выбери тип дежурства:",
        reply_markup=shift_keyboard()
    )


async def choose_location(update: Update, context: ContextTypes.DEFAULT_TYPE):

    tg_id = update.effective_user.id
    location_text = update.message.text

    if location_text == "🖥 Кластер":
        location = "cluster"
    elif location_text == "💬 RocketChat":
        location = "rocketchat"
    else:
        return

    now = datetime.now(TZ)

    async with SessionLocal() as session:

        user = await session.get(User, tg_id)

        if not user:
            await update.message.reply_text("Сначала нажми /start")
            return

        shift = Shift(
            user_id=tg_id,
            start_time=now,
            location=location
        )

        session.add(shift)
        await session.commit()

    await update.message.reply_text(
        f"✅ Смена началась\n📍 {location_text}\n⏰ {now.strftime('%H:%M')}",
        reply_markup=main_keyboard()
    )


async def left(update: Update, context: ContextTypes.DEFAULT_TYPE):

    tg_id = update.effective_user.id
    now = datetime.now(TZ)

    async with SessionLocal() as session:

        shift = await Shift.get_active_shift(session, tg_id)

        if not shift:
            await update.message.reply_text(
                "⚠️ У тебя нет активной смены.",
                reply_markup=main_keyboard()
            )
            return

        shift.end_time = now

        duration_minutes = int(
            (shift.end_time - shift.start_time).total_seconds() / 60
        )

        hours = duration_minutes // 60
        minutes = duration_minutes % 60

        await session.commit()

        user = await session.get(User, tg_id)

    try:
        await log_shift_to_sheet(
            tg_id=tg_id,
            platform_nick=user.platform_nick,
            start=shift.start_time,
            end=shift.end_time,
            duration=f"{hours}:{minutes:02d}",
            location=shift.location
        )
    except Exception as e:
        print("Google Sheets error:", e)

    await update.message.reply_text(
        f"🏁 Смена завершена!\n⏳ Отработано: {hours}:{minutes:02d}",
        reply_markup=main_keyboard()
    )
