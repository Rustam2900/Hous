all_languages = ['ru', 'en']

message_history = {}

default_languages = {
    "language_not_found": "You have not selected the correct language!\n"
                          "Вы не выбрали правильный язык!",
    "welcome_message": "Hello, welcome to our bot!\n"
                       "Choose one of the languages below!\n\n"
                       "Здравствуйте, добро пожаловать в наш бот!\n"
                       "Выберите один из языков ниже!",

    "en": {
        "filter": "filter the homes that suit you",
        "zipcode": "zipcode",
        "min_sum_prompt": "Please enter the minimum amount (e.g., 2000$):",
        "max_sum_prompt": "Please enter the maximum amount (e.g., 5000$):",
        "invalid_room": "Invalid input. Please enter a valid number of rooms.",
        "invalid_sum": "Invalid input. Please enter a valid amount.",
        "summary": "Summary:\n\nRooms: {room}\n\nzipcode: {zipcode}\n\n"
                   "Minimum sum: {min_sum}\n\nMaximum sum: {max_sum}",
        "room_prompt": "Please enter the number of rooms:",
        "sorry": "Sorry, please try another number",
        "address": "address",
        "order_list": "orders",
        "price": "price",
        "order_number": "order number",
        "enter_number": "Please enter a number!",
        "order_address": "Please enter your address:",
        "order_created": "Order created",
        "order_not_created": "Order not created!",
        "order_not_found": "Order not found!",
        "order": "My orders",
        "full_name": "Please enter your full name",
        "registration": "Registration",
        "login": "Login",
        "logout": "↩️ logout",
        "exit": "You have logged out of your account",
        "sign_password": "Please enter your password",
        "successful_registration": "Successfully registered",
        "successful_login": "Successfully logged in",
        "user_not_found": "User not found",
        "contact": "Please enter your phone number",
        "share_contact": "Share contact",
        "password": "Please enter a password for your account",
        "settings": "⚙️ Settings",
        "contact_us": "📲 Contact us",
        "my_orders": "📦 My orders",
        "create_order": "✅ Place an order",
        "cancel": "❌ Cancel",
        'categories': 'Categories',
        "view_products": "🛒view_products ",
        "select_language": "Select a language!",
        "successful_changed": "Successfully changed",
        "contact_us_message": "Our address:\n{}\n\n"
                              "Contact us:\n{}\n{}\n\n"
                              "Contact hours:\n{}"

    },

    "ru": {
        "filter": "отфильтруйте дома, которые вам подходят",
        "zipcode": "почтовый индекс",
        "summary": "Сводка:\n\nКомнаты: {room}\n\nпочтовый индекс: {zipcode}"
                   "\n\nМинимальная сумма: {min_sum}\n\nМаксимальная сумма: {max_sum}",
        "invalid_sum": "Недопустимый ввод. Введите допустимую сумму.",
        "invalid_room": "максимальная суммаНедопустимый ввод. Введите допустимое количество комнат.",
        "max_sum_prompt": "Пожалуйста, введите максимальную сумму (например, 5000$):",
        "min_sum_prompt": "Пожалуйста, введите минимальную сумму (например, 2000$):",
        "room_prompt": "Пожалуйста, введите количество комнат:",
        "sorry": "Извините, пожалуйста, попробуйте другой номер",
        "address": "адрес",
        "order_list": "заказы",
        "price": "цена",
        "order_number": "номер заказа",
        "enter_number": "Пожалуйста, введите номер!",
        "order_address": "Пожалуйста, введите ваш адрес:",
        "order_created": "Заказ создан",
        "order_not_created": "Заказ не создан!",
        "order_not_found": "Заказ не найден!",
        "order": "Мои заказы",
        "full_name": "Пожалуйста, введите ваше полное имя",
        "registration": "Регистрация",
        "login": "Вход",
        "logout": "↩️ выход",
        "exit": "Вы вышли из своей учетной записи",
        "sign_password": "Пожалуйста, введите ваш пароль",
        "successful_registration": "Успешная регистрация",
        "successful_login": "Успешный вход",
        "user_not_found": "Пользователь не найден",
        "contact": "Пожалуйста, введите ваш номер телефона",
        "share_contact": "Поделиться контактом",
        "password": "Пожалуйста, введите пароль для вашей учетной записи",
        "settings": "⚙️ Настройки",
        "contact_us": "📲 Связаться с нами",
        "my_orders": "📦 Мои заказы",
        "create_order": "✅ Сделать заказ",
        "cancel": "❌ Отменить",
        'categories': 'Категории',
        "view_products": "🛒Посмотреть товары",
        "select_language": "Выберите язык!",
        "successful_changed": "Успешно изменено",
        "contact_us_message": "Наш адрес:\n{}\n\n"
                              "Связаться с нами:\n{}\n{}\n\n"
                              "Часы работы:\n{}"
    }
}

user_languages = {}
local_user = {}

introduction_template = {
    'ru':
        """
    👕 Магазин Sneaker World <a href="https://t.me/sneaker_world_bot">Sneaker World</a> представляет!

    Что может сделать бот?

    Заказ одежды
    Информация о последних модных трендах
    Проверка счетов
    Будьте в курсе эксклюзивных скидок и акций
    Вопросы и помощь
    🌐 SneakerBot - легкий и быстрый сервис!

    🏠 Оставайтесь дома и пользуйтесь уникальными услугами!

    🟢 Присоединяйтесь прямо сейчас: <a href="https://t.me/sneaker_world_bot">Sneaker World</a>
    ✉️ Телеграм канал: <a href="https://t.me/sneaker_world_bot">Sneaker World</a>

    Sneaker World - Ваш стиль!
    """,

    "en":

        """
    👕 Sneaker World shop <a href="https://t.me/sneaker_world_bot">Sneaker World</a> presents!

    What can the bot do?

    Place clothing orders
    Get information about the latest fashion trends
    Check accounts
    Stay informed about exclusive discounts and promotions
    Questions and assistance
    🌐 SneakerBot - an easy and quick service!

    🏠 Stay at home and enjoy unique services!

    🟢 Join now: <a href="https://t.me/sneaker_world_bot">Sneaker World</a>
    ✉️ Telegram channel: <a href="https://t.me/sneaker_world_bot">Sneaker World</a>

    Sneaker World - Your Style!

    """
}

bot_description = """
    👕 This bot is designed for you to order from the Sneaker World online store at any time from home and access various services. 👕

 - - - - - - - - - - - - - - - - - - - - - - - - - 

   👕Этот бот создан для того, чтобы вы могли заказывать в интернет-магазине Sneaker World в любое время из дома и пользоваться услугами👕
"""

order_text = {
    "en": "Order number {} \n order status {}",
    "ru": "Номер заказа {} \n Статус заказа {}"
}


def fix_phone(phone):
    if "+" not in phone:
        return f"+{phone}"
    return phone
