import re

from aiogram.client.default import DefaultBotProperties
from django.conf import settings
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram import Dispatcher, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards import get_languages, get_main_menu
from bot.models import User
from bot.utils import default_languages, introduction_template






dp = Dispatcher()
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

phone_number_validator = re.compile(r'^\+998 \d{2} \d{3} \d{2} \d{2}$')



@dp.message(CommandStart())
async def welcome(message: Message):
    user_id = message.from_user.id
    user = await User.objects.filter(telegram_id=user_id).afirst()

    if user and user.user_lang:
        main_menu_markup = get_main_menu(user.user_lang)
        await message.answer(
            text=introduction_template[user.user_lang],
            reply_markup=main_menu_markup
        )
    else:
        msg = default_languages['welcome_message']
        await message.answer(msg, reply_markup=get_languages())
