from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from bot.utils import default_languages


def get_languages(flag="lang"):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ru 🇷🇺", callback_data=f"{flag}_ru"),
         InlineKeyboardButton(text="en 🇺🇸", callback_data=f"{flag}_en")],
    ])
    return keyboard


def get_main_menu(language):
    main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="For Sale", callback_data="sale"),
            InlineKeyboardButton(text="For Rent", callback_data="rent")
        ]
    ])
    return main_menu_keyboard
