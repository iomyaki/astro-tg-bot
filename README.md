# Тестовое задание в Stomodomo Group

Написать телеграм-бота “Гороскоп” на Python, используя библиотеку aiogram, со следующим функционалом:
- При регистрации бот предлагает пользователю выбрать свой знак зодиака. Используется ReplyKeyboardMarkup 3 ряда по 4 кнопки с эмоджи знака зодиака. После выбора знака бот присылает сообщение с информацией о выбранном знаке.
- После регистрации бот присылает гороскоп на сегодня. Сообщение включает себя текст, картинку и InlineKeyboardMarkup с одной кнопкой “Обновить”. Текст включает в себя дату гороскопа, выделенную жирным шрифтом. При нажатии на кнопку сообщение должно обновиться, и прогноз должен измениться на другой.
- Каждый день в 10 утра пользователь получает гороскоп на новый день (только в случае, если его еще нет).
- В меню бота есть команда “/update”, которая обновляет прогноз на сегодня (аналогично кнопке “Обновить” в сообщении) либо отправляет новое сообщение с гороскопом, если сообщения за сегодня по какой-то причине нет.
- Когда пользователь отправляет что угодно в чат, бот пишет “Извините, я не понял”.
- Добавить в меню бота команду “/change_zodiac”. При нажатии появляется клавиатура, как при регистрации, и знак зодиака пользователя меняется на выбранный. Приходит новый гороскоп на сегодня.
- Добавить в меню бота команду “/clear_history”, которая очищает историю сообщений, оставляя только сообщение с последним выбранным знаком зодиака.

Разворачивать бота на сервере не нужно, достаточно прислать код с локальным запуском.
