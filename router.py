import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from app import database as db
from app import kb
from script import send_horoscope

r = Router()
zodiac_latin = {
    "♒": "aquarius",
    "♓": "pisces",
    "♈": "aries",
    "♉": "taurus",
    "♊": "gemini",
    "♋": "cancer",
    "♌": "leo",
    "♍": "virgo",
    "♎": "libra",
    "♏": "scorpio",
    "♐": "sagittarius",
    "♑": "capricorn",
}
zodiac_ru = {
    "♒": " водолеях",
    "♓": " рыбах",
    "♈": "б овнах",
    "♉": " тельцах",
    "♊": " близнецах",
    "♋": " раках",
    "♌": " львах",
    "♍": " девах",
    "♎": " весах",
    "♏": " скорпионах",
    "♐": " стрельцах",
    "♑": " козерогах",
}


@r.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Приветствую! Выберите свой знак зодиака:", reply_markup=kb.choose_zodiac())


@r.message(Command("update"))
async def perform_update(message: Message) -> None:
    bot = message.bot
    user_id = message.from_user.id

    if await db.get_sent_today(user_id):
        await bot.delete_message(chat_id=message.chat.id, message_id=await db.get_last_horoscope_msg(user_id))
    await send_horoscope(user_id)


@r.message(Command("change_zodiac"))
async def change_zodiac(message: Message) -> None:
    await message.answer("Выберите новый знак зодиака:", reply_markup=kb.choose_zodiac())


@r.message(Command("clear_history"))
async def clear_history(message: Message) -> None:
    user_id = message.from_user.id
    bot = message.bot

    first_message = await db.get_first_message(user_id)
    last_zodiac = await db.get_last_zodiac_msg(user_id)

    for idx in range(first_message, message.message_id + 1):
        if idx != last_zodiac:
            try:
                await bot.delete_message(message.chat.id, idx)
            except Exception as e:
                logging.info(f"Не удалось удалить сообщение #{idx}: {e}")

    await db.set_first_message(user_id, last_zodiac)


@r.callback_query(lambda call: call.data == "renew_horoscope")
async def renew_horoscope(call: CallbackQuery) -> None:
    bot = call.bot
    user_id = call.from_user.id

    await bot.delete_message(chat_id=call.message.chat.id, message_id=await db.get_last_horoscope_msg(user_id))
    await send_horoscope(user_id)


@r.message(lambda message: message.text in {"♒", "♓", "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑"})
async def zodiac_info(message: Message) -> None:
    latin_name = zodiac_latin[message.text]
    russian_name = zodiac_ru[message.text]

    user_id = message.from_user.id
    await db.set_zodiac(user_id, latin_name)
    last_zodiac_message = await message.answer(f"Информация о{russian_name}", reply_markup=ReplyKeyboardRemove())
    await send_horoscope(user_id)

    await db.set_last_zodiac_msg(user_id, last_zodiac_message.message_id)


@r.message()
async def answer(message: Message) -> None:
    await message.answer("Извините, я не понял")
