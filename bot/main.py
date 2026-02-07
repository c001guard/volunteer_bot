from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from bot.config import BOT_TOKEN
from bot.database.models import Base
from bot.database.db import init_db

from bot.handlers.start import start
from bot.handlers.language import set_language
from bot.handlers.shifts import arrived, choose_location, left


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 🔥 Инициализация БД через lifecycle PTB
    async def on_startup(app):
        await init_db(Base)
        print("DB CONNECTED")

    app.post_init = on_startup

    # handlers
    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("^(Русский|O'zbekcha)$"),
            set_language
        )
    )

    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^🟢 Пришёл$"), arrived)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("^(🖥 Кластер|💬 RocketChat)$"),
            choose_location
        )
    )

    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^🔴 Ушёл$"), left)
    )

    print("BOT STARTED 🚀")

    # ❗ ВАЖНО — без await
    app.run_polling()


if __name__ == "__main__":
    main()
