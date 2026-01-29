import logging
import sqlite3
from datetime import datetime, timezone, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ================= НАСТРОЙКИ =================

TOKEN = "8010848066:AAE4lysx6-eZxbQA-KCbhi6AWSc_0ydWsq0"
SPREADSHEET_ID = "1hNXRVjX0dfETIf3O9jXWmmRWMQOV3w7SY-Ye_zE_rBc"
CREDS_FILE = "creds.json"
DB_FILE = "data/volunteers.db"

TZ = timezone(timedelta(hours=5))  # Ташкент
ADMIN_CONTACT = "@c001ermsc"

logging.basicConfig(level=logging.INFO)

# ================= GOOGLE SHEETS =================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# ================= DATABASE =================

db = sqlite3.connect(DB_FILE, check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    platform_nick TEXT UNIQUE,
    start_time TEXT,
    role TEXT DEFAULT 'user'
)
""")
db.commit()

# ================= HELPERS =================

def get_user(tg_id):
    cur.execute("SELECT telegram_id, platform_nick, start_time, role FROM users WHERE telegram_id=?", (tg_id,))
    return cur.fetchone()

def is_allowed(tg_id):
    user = get_user(tg_id)
    print(f"[ACCESS CHECK] {tg_id} -> {user}")
    return user is not None

def is_admin(tg_id):
    user = get_user(tg_id)
    return user and user[3] == "admin"

def add_user(tg_id, nick, role="user"):
    cur.execute(
        "INSERT OR REPLACE INTO users (telegram_id, platform_nick, start_time, role) VALUES (?, ?, NULL, ?)",
        (tg_id, nick, role)
    )
    db.commit()

def delete_user(nick):
    cur.execute("DELETE FROM users WHERE platform_nick=?", (nick,))
    db.commit()

def set_start_time(tg_id, time_str):
    cur.execute("UPDATE users SET start_time=? WHERE telegram_id=?", (time_str, tg_id))
    db.commit()

def clear_start_time(tg_id):
    cur.execute("UPDATE users SET start_time=NULL WHERE telegram_id=?", (tg_id,))
    db.commit()

# ================= FSM =================

class EditState(StatesGroup):
    choose_field = State()
    waiting_for_time = State()

class AdminState(StatesGroup):
    menu = State()
    waiting_for_nick = State()

# ================= BOT =================

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# ================= MIDDLEWARE (ТУРНИКЕТ) =================

class AccessMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        tg_id = message.from_user.id
        if not is_allowed(tg_id):
            await message.answer(
                "⛔ Доступ запрещён.\n"
                f"Обратитесь к администратору: {ADMIN_CONTACT}"
            )
            raise CancelHandler()

dp.middleware.setup(AccessMiddleware())

# ================= KEYBOARDS =================

def main_keyboard(is_admin=False):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🟢 Пришёл", "🔴 Ушёл")
    kb.add("✏️ Исправить время")
    if is_admin:
        kb.add("⚙️ Админ панель")
    return kb

edit_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
edit_keyboard.add("⏰ Время прихода")
edit_keyboard.add("❌ Отмена")

admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add("➕ Добавить пользователя", "➖ Удалить пользователя")
admin_keyboard.add("📋 Список пользователей")
admin_keyboard.add("⬅️ Назад")

# ================= HANDLERS =================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        f"Привет, {user[1]} 👋",
        reply_markup=main_keyboard(is_admin(message.from_user.id))
    )

@dp.message_handler(lambda m: m.text == "🟢 Пришёл")
async def arrived(message: types.Message):
    user = get_user(message.from_user.id)
    if user[2]:
        await message.answer("Ты уже отметил приход ⏳")
        return

    now = datetime.now(TZ).isoformat()
    set_start_time(message.from_user.id, now)
    await message.answer(f"Приход зафиксирован: {datetime.now(TZ).strftime('%H:%M')} 🟢")

@dp.message_handler(lambda m: m.text == "🔴 Ушёл")
async def left(message: types.Message):
    user = get_user(message.from_user.id)
    if not user[2]:
        await message.answer("Ты ещё не отмечал приход 😅")
        return

    start = datetime.fromisoformat(user[2])
    end = datetime.now(TZ)
    delta = end - start

    minutes = int(delta.total_seconds() // 60)
    hours = minutes // 60
    mins = minutes % 60
    duration = f"{hours}:{mins:02d}"

    sheet.append_row([
        user[1],
        start.strftime("%Y-%m-%d %H:%M"),
        end.strftime("%Y-%m-%d %H:%M"),
        duration
    ])

    clear_start_time(message.from_user.id)
    await message.answer(f"Дежурство завершено 🫡\nОтработано: {duration}")

# ================= РЕДАКТИРОВАНИЕ ВРЕМЕНИ =================

@dp.message_handler(lambda m: m.text == "✏️ Исправить время")
async def edit_time(message: types.Message):
    await message.answer("Что хочешь изменить?", reply_markup=edit_keyboard)
    await EditState.choose_field.set()

@dp.message_handler(state=EditState.choose_field)
async def choose_edit_field(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.finish()
        await message.answer("Отменено.", reply_markup=main_keyboard(is_admin(message.from_user.id)))
        return

    await state.update_data(field=message.text)
    await message.answer("Введи новое время в формате HH:MM")
    await EditState.waiting_for_time.set()

@dp.message_handler(state=EditState.waiting_for_time)
async def set_new_time(message: types.Message, state: FSMContext):
    try:
        h, m = map(int, message.text.split(":"))
        new_time = datetime.now(TZ).replace(hour=h, minute=m, second=0, microsecond=0)
    except:
        await message.answer("Неверный формат. Пример: 09:30")
        return

    set_start_time(message.from_user.id, new_time.isoformat())
    await state.finish()
    await message.answer("Время прихода обновлено ✅", reply_markup=main_keyboard(is_admin(message.from_user.id)))

# ================= АДМИН ПАНЕЛЬ =================

@dp.message_handler(lambda m: m.text == "⚙️ Админ панель")
async def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Админ панель:", reply_markup=admin_keyboard)
    await AdminState.menu.set()

@dp.message_handler(state=AdminState.menu)
async def admin_menu(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.finish()
        await message.answer("Выход.", reply_markup=main_keyboard(True))

    elif message.text == "📋 Список пользователей":
        cur.execute("SELECT platform_nick, role FROM users")
        users = cur.fetchall()
        text = "Пользователи:\n"
        for u in users:
            text += f"- {u[0]} ({u[1]})\n"
        await message.answer(text)

    elif message.text == "➕ Добавить пользователя":
        await message.answer("Отправь Telegram ID пользователя:")
        await AdminState.waiting_for_nick.set()

    elif message.text == "➖ Удалить пользователя":
        await message.answer("Отправь ник пользователя для удаления:")
        await AdminState.waiting_for_nick.set()

@dp.message_handler(state=AdminState.waiting_for_nick)
async def admin_manage_user(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text.isdigit():
        await state.update_data(tg_id=int(text))
        await message.answer("Теперь отправь ник платформы:")
    else:
        data = await state.get_data()
        tg_id = data.get("tg_id")
        add_user(tg_id, text)
        await message.answer(f"Пользователь {text} добавлен ✅")
        await state.finish()
        await message.answer("Админ панель:", reply_markup=admin_keyboard)

# ================= RUN =================

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
