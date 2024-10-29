import sqlite3 as sq


with sq.connect("app/astro_bot.db") as db:
    cur = db.cursor()


async def db_start() -> None:
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER NOT NULL PRIMARY KEY, zodiac TEXT, "
                "sent_today INTEGER, last_zodiac_msg INTEGER, last_horoscope_msg INTEGER, last_prediction INTEGER, "
                "first_message INTEGER, last_message INTEGER);")
    db.commit()


async def check_user(user_id: int) -> int:
    cur.execute(f"SELECT user_id FROM users WHERE user_id = {user_id};")
    return cur.fetchone()


async def set_zodiac(user_id: int, sign: str) -> None:
    if not await check_user(user_id):
        cur.execute(f"INSERT INTO users VALUES ({user_id}, '{sign}', 0, -1, -1, -1, 1, -1);")
    else:
        cur.execute(f"UPDATE users SET zodiac = '{sign}' WHERE user_id = {user_id};")
    db.commit()


async def get_zodiac(user_id: int) -> str:
    if not await check_user(user_id):
        raise ValueError
    else:
        cur.execute(f"SELECT zodiac FROM users WHERE user_id = {user_id};")
    return cur.fetchone()[0]


async def set_first_message(user_id: int, ident: int) -> None:
    cur.execute(f"UPDATE users SET first_message = {ident} WHERE user_id = {user_id}")
    db.commit()


async def get_first_message(user_id: int) -> int:
    cur.execute(f"SELECT first_message FROM users WHERE user_id = {user_id}")
    return int(cur.fetchone()[0])


async def set_last_message(user_id: int, ident: int) -> None:
    cur.execute(f"UPDATE users SET last_message = {ident} WHERE user_id = {user_id}")
    db.commit()


async def get_last_message(user_id: int) -> int:
    cur.execute(f"SELECT last_message FROM users WHERE user_id = {user_id}")
    return int(cur.fetchone()[0])


async def set_sent_today(user_id: int) -> None:
    if not await check_user(user_id):
        raise ValueError
    else:
        cur.execute(f"UPDATE users SET sent_today = 1 WHERE user_id = {user_id};")
    db.commit()


async def reset_sent_today() -> None:
    cur.execute("UPDATE users SET sent_today = 0")
    db.commit()


async def get_sent_today(user_id: int) -> bool:
    if not await check_user(user_id):
        raise ValueError
    else:
        cur.execute(f"SELECT sent_today FROM users WHERE user_id = {user_id};")

    return True if cur.fetchone()[0] == 1 else False


async def get_users_for_daily() -> list:
    cur.execute(f"SELECT user_id FROM users WHERE sent_today = 0")
    return cur.fetchall()


async def set_last_zodiac_msg(user_id: int, ident: int) -> None:
    if not await check_user(user_id):
        raise ValueError
    else:
        cur.execute(f"UPDATE users SET last_zodiac_msg = {ident} WHERE user_id = {user_id};")
    db.commit()


async def get_last_zodiac_msg(user_id: int) -> int:
    if not await check_user(user_id):
        raise ValueError
    else:
        cur.execute(f"SELECT last_zodiac_msg FROM users WHERE user_id = {user_id};")
    return int(cur.fetchone()[0])


async def set_last_horoscope_msg(user_id: int, ident: int) -> None:
    if not await check_user(user_id):
        raise ValueError
    else:
        cur.execute(f"UPDATE users SET last_horoscope_msg = {ident} WHERE user_id = {user_id};")
    db.commit()


async def get_last_horoscope_msg(user_id: int) -> int:
    if not await check_user(user_id):
        raise ValueError
    else:
        cur.execute(f"SELECT last_horoscope_msg FROM users WHERE user_id = {user_id};")
    return int(cur.fetchone()[0])


async def set_last_prediction(user_id: int, ident: int) -> None:
    if not await check_user(user_id):
        raise ValueError
    else:
        cur.execute(f"UPDATE users SET last_prediction = {ident} WHERE user_id = {user_id};")
    db.commit()


async def get_last_prediction(user_id: int) -> int:
    if not await check_user(user_id):
        raise ValueError
    else:
        cur.execute(f"SELECT last_prediction FROM users WHERE user_id = {user_id};")
    return int(cur.fetchone()[0])
