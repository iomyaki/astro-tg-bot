from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def choose_zodiac() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="♒"),  # водолей, aquarius
                KeyboardButton(text="♓"),  # рыбы, pisces
                KeyboardButton(text="♈"),  # овен, aries
                KeyboardButton(text="♉"),  # телец, taurus
            ],
            [
                KeyboardButton(text="♊"),  # близнецы, gemini
                KeyboardButton(text="♋"),  # рак, cancer
                KeyboardButton(text="♌"),  # лев, leo
                KeyboardButton(text="♍"),  # дева, virgo
            ],
            [
                KeyboardButton(text="♎"),  # весы, libra
                KeyboardButton(text="♏"),  # скорпион, scorpio
                KeyboardButton(text="♐"),  # стрелец, sagittarius
                KeyboardButton(text="♑"),  # козерог, capricorn
            ],
        ],
        resize_keyboard=True
    )


def renew() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Обновить",
                    callback_data="renew_horoscope",)
            ]
        ]
    )
