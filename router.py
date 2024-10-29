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
    await db.set_last_message(message.from_user.id, message.message_id)


@r.message(Command("update"))
async def perform_update(message: Message) -> None:
    bot = message.bot
    user_id = message.from_user.id

    if await db.get_sent_today(user_id):
        await bot.delete_message(chat_id=message.chat.id, message_id=await db.get_last_horoscope_msg(user_id))
    last_horoscope_id = await send_horoscope(user_id)

    await db.set_last_horoscope_msg(user_id, last_horoscope_id)
    await db.set_sent_today(user_id)
    await db.set_last_message(message.from_user.id, message.message_id)


@r.message(Command("change_zodiac"))
async def change_zodiac(message: Message) -> None:
    await message.answer("Выберите новый знак зодиака:", reply_markup=kb.choose_zodiac())
    await db.set_last_message(message.from_user.id, message.message_id)


@r.message(Command("clear_history"))
async def clear_history(message: Message) -> None:
    user_id = message.from_user.id
    bot = message.bot

    first = await db.get_first_message(user_id)
    last = await db.get_last_message(user_id)
    saved = await db.get_last_zodiac_msg(user_id)

    for idx in range(first, last + 3):
        if idx != saved:
            try:
                await bot.delete_message(message.chat.id, idx)
            except Exception as e:
                logging.info(f"Не удалось удалить сообщение #{idx}: {e}")

    await db.set_first_message(user_id, message.message_id + 1)
    await db.set_last_message(user_id, message.message_id + 1)


@r.callback_query(lambda call: call.data == "renew_horoscope")
async def renew_horoscope(call: CallbackQuery):
    bot = call.bot
    user_id = call.from_user.id

    await bot.delete_message(chat_id=call.message.chat.id, message_id=await db.get_last_horoscope_msg(user_id))
    last_horoscope_id = await send_horoscope(user_id)

    await db.set_last_horoscope_msg(user_id, last_horoscope_id)
    await db.set_sent_today(user_id)
    await db.set_last_message(call.from_user.id, call.message_id)


@r.message(lambda message: message.text in {"♒", "♓", "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑"})
async def zodiac_info(message: Message) -> None:
    latin_name = zodiac_latin[message.text]
    russian_name = zodiac_ru[message.text]

    user_id = message.from_user.id
    await db.set_zodiac(user_id, latin_name)
    last_zodiac_message = await message.answer(f"Информация о{russian_name}", reply_markup=ReplyKeyboardRemove())
    last_horoscope_message_id = await send_horoscope(user_id)

    await db.set_last_zodiac_msg(user_id, last_zodiac_message.message_id)
    await db.set_last_horoscope_msg(user_id, last_horoscope_message_id)
    await db.set_sent_today(user_id)
    await db.set_last_message(message.from_user.id, message.message_id)


@r.message()
async def answer(message: Message):
    await message.answer("Извините, я не понял")
    await db.set_last_message(message.from_user.id, message.message_id)
