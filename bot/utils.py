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
        "user_not": "User not found. Please register first.",
        "county_user_not": "No houses available in your selected county within your budget.",
        "county_user_update": "No county selected. Please update your profile with a county.",
        "state_": "Choose a state:",
        "country": "Please select a county:",
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
        "user_not": "Пользователь не найден. Пожалуйста, зарегистрируйтесь сначала.",
        "county_user_not": "В выбранном вами округе нет домов, соответствующих вашему бюджету.",
        "county_user_update": "Округ не выбран. Пожалуйста, обновите свой профиль, указав округ.",
        "state_": "Выберите штат:",
        "country": "Пожалуйста, выберите округ:",
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
    🏠 HomeFinder Bot - Найти новый дом стало проще,
     чем когда-либо, не выходя из дома!

    🎯 Что можно сделать?

    Искать дома для аренды или покупки
    Выбирать дома, комнаты и цены, которые
    соответствуют вашим предпочтениям
    Получать информацию в реальном времени
    о домах, которые подходят вашему бюджету
    Получать уведомления о новых объявлениях и предложениях
    ✨ HomeFinder Bot поможет вам найти идеальный дом!
    🔔 Уведомления: Каждый раз, когда добавляется новое объявление,
    бот отправит вам уведомление с лучшими предложениями.

    🌐 Начните сейчас: <a href="https://t.me/SamItGlobalHousBot">HomeFinder Bot</a>
    """,

    "en":

        """
    🏠 HomeFinder Bot - Finding a new home has never
     been easier from the comfort of your own home!

    🎯 What can you do?

    Search for houses to rent or buy
    Choose homes, rooms, and prices that match
    your preferences
    Get real-time information on homes that fit your budget
    Receive notifications about new listings and offers 
    ✨ HomeFinder Bot helps you find the perfect home!
    🔔 Notifications: Every time a new listing is added,
     the bot will notify you with the best offers.

    🌐 Start now: <a href="https://t.me/SamItGlobalHousBot">HomeFinder Bot</a>

    """
}


def fix_phone(phone):
    if "+" not in phone:
        return f"+{phone}"
    return phone
