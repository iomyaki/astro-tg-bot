import random
from datetime import datetime

from aiogram import Bot, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

import config
from app import database as db
from app import kb


bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
predictions = [
    "не стоит выходить из комнаты",
    "рекомендовано съесть ещё этих мягких французских булок, да выпить чаю",
    "хорошо бы подумать, быть или не быть",
    "надо найти актуальный инфоповод",
    "советуем избежать встречи с самим собой из прошлого",
    "звёзды велят всё успеть до дедлайна",
    "точно нужно выйти потрогать траву",
]
zodiac_dative = {
    "aquarius": "водолеям",
    "pisces": "рыбам",
    "aries": "овнам",
    "taurus": "тельцам",
    "gemini": "близнецам",
    "cancer": "ракам",
    "leo": "львам",
    "virgo": "девам",
    "libra": "весам",
    "scorpio": "скорпионам",
    "sagittarius": "стрельцам",
    "capricorn": "козерогам",
}
img_path = "https://images.newscientist.com/wp-content/uploads/2024/08/19104831/SEI_217496619.jpg?width=1003"


async def set_bot_commands() -> None:
    commands = [
        BotCommand(command="start", description="Начать взаимодействие с ботом"),
        BotCommand(command="update", description="Получить или обновить прогноз на сегодня"),
        BotCommand(command="change_zodiac", description="Изменить свой знак зодиака"),
        BotCommand(command="clear_history", description="Очистить историю сообщений"),
    ]
    await bot.set_my_commands(commands)


async def send_horoscope(user_id: int) -> None:
    last_prediction_id = await db.get_last_prediction(user_id)

    n = len(predictions)
    new_prediction_id = random.choice(range(n))
    while new_prediction_id == last_prediction_id:
        new_prediction_id = random.choice(range(n))

    prediction = predictions[new_prediction_id]
    await db.set_last_prediction(user_id, new_prediction_id)

    sign_dative = zodiac_dative[await db.get_zodiac(user_id)]
    today_date = datetime.today().strftime('%d.%m.%Y')
    caption = f"Сегодня, {html.bold(today_date)}, {sign_dative} {prediction}"

    message = await bot.send_photo(
        chat_id=user_id,
        photo=img_path,
        caption=caption,
        reply_markup=kb.renew(),
    )
    message_id = message.message_id

    await db.set_last_horoscope_msg(user_id, message_id)
    await db.set_last_message(user_id, message_id)


async def daily_horoscope() -> None:
    users = await db.get_users_for_daily()
    for user in users:
        await send_horoscope(user[0])
