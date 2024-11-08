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
from bot.db import save_user_language
from bot.utils import user_languages
from bot.states import UserStates





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

@dp.callback_query(lambda call: call.data.startswith("lang"))
async def get_query_languages(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_lang = call.data.split("_")[1]
    user_languages[user_id] = user_lang

    await save_user_language(user_id, user_lang)

    await bot.answer_callback_query(call.id)
    await state.set_state(UserStates.name)

    text = default_languages[user_lang]['full_name']
    await call.message.answer(text, reply_markup=None)