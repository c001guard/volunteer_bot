from telegram import ReplyKeyboardMarkup


def language_keyboard():
    return ReplyKeyboardMarkup(
        [["Русский", "O'zbekcha"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["🟢 Пришёл", "🔴 Ушёл"]
        ],
        resize_keyboard=True
    )


def shift_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["🖥 Кластер", "💬 RocketChat"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
