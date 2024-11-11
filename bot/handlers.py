import re

from aiogram.client.default import DefaultBotProperties
from django.conf import settings
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram import Dispatcher, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from asgiref.sync import sync_to_async

from bot.keyboards import get_languages, get_main_menu
from bot.models import User
from bot.utils import default_languages, introduction_template
from bot.db import (save_user_language, save_user_info_to_db, fix_phone,
                    get_user_language, state_get, county_get, create_or_update_user_state,
                    create_or_update_user_country, save_user_info_to_db_create)
from bot.utils import user_languages
from bot.states import UserStates, UserHousStates

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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


@dp.message(UserStates.name)
async def reg_user_contact(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = user_languages.get(user_id, 'en')

    await state.update_data(name=message.text)
    await state.set_state(UserStates.contact)

    text = default_languages.get(user_lang, {}).get('contact', 'Please enter your phone number')
    await message.answer(text)


@dp.message(UserStates.contact)
async def company_contact(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = user_languages.get(user_id, 'en')

    if message.contact:
        phone = fix_phone(message.contact.phone_number)
    else:
        phone = fix_phone(message.text)

    if not phone_number_validator.match(phone):
        error_message = default_languages[user_lang].get(
            "enter_number", "Please enter a valid phone number format: +998 XX XXX XX XX"
        )
        await message.answer(error_message)
        return

    await state.update_data(company_contact=phone)

    state_data = await state.get_data()
    user_data = {
        "full_name": state_data.get('name'),
        "phone_number": phone,
        "username": message.from_user.username,
        "user_lang": user_lang,
        "telegram_id": user_id,
        "tg_username": f"https://t.me/{message.from_user.username}",
    }

    try:
        await save_user_info_to_db(user_data)
        success_message = default_languages[user_lang].get("successful_registration",
                                                           "Thank you, registration successful!")
        await message.answer(text=success_message, reply_markup=get_main_menu(user_lang))

    except Exception as e:
        error_message = default_languages[user_lang].get("sorry", "Error: Registration failed!")
        await message.answer(text=error_message)

    await state.clear()


@dp.callback_query(lambda call: call.data in ["sale", "rent"])
async def handle_products_by_category(call: CallbackQuery):
    user_id = call.from_user.id
    user_lang = await get_user_language(user_id)

    states = await state_get()
    inline_kb = InlineKeyboardMarkup(row_width=3, inline_keyboard=[])
    inline_buttons = []

    for state in states:
        state_name = state.name_ru if user_lang == 'ru' else state.name_en
        inline_buttons.append(InlineKeyboardButton(text=state_name or "no name", callback_data=f"state_{state.id}"))

    inline_kb.inline_keyboard = [inline_buttons[i:i + 3] for i in range(0, len(inline_buttons), 3)]
    await call.message.edit_text("Choose a state::", reply_markup=inline_kb)


@dp.callback_query(lambda call: call.data.startswith("state_"))
async def handle_products_by_category(call: CallbackQuery):
    user_id = call.from_user.id
    user_lang = await get_user_language(user_id)
    state_id = int(call.data.split("_")[1])

    counties = await county_get(state_id)

    inline_kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[])
    inline_buttons = []

    for county in counties:
        country_name = county.name_ru if user_lang == 'ru' else county.name_en
        inline_buttons.append(
            InlineKeyboardButton(text=country_name or "no name", callback_data=f"country_{county.id}"))

    inline_kb.inline_keyboard = [inline_buttons[i:i + 2] for i in range(0, len(inline_buttons), 2)]
    await call.message.edit_text("Please select a county:", reply_markup=inline_kb)
    user, created = await create_or_update_user_state(
        telegram_id=user_id,
        state_id=state_id
    )


@dp.callback_query(lambda call: call.data.startswith("country_"))
async def handle_county_selection(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_lang = await get_user_language(user_id)

    county_id = int(call.data.split("_")[1])
    print("###", county_id)
    user, created = await create_or_update_user_country(
        telegram_id=user_id,
        county_id=county_id
    )
    await state.set_state(UserHousStates.room)
    text = default_languages[user_lang]['room_prompt']
    await call.message.answer(text, reply_markup=None)


@dp.message(UserHousStates.room)
async def ask_min_sum(message: Message, state: FSMContext):
    user_lang = await get_user_language(message.from_user.id)
    text = default_languages[user_lang]['invalid_room']

    try:
        room_count = int(message.text)
    except ValueError:
        await message.answer(text=text)
        return

    await state.update_data(room=room_count)

    await state.set_state(UserHousStates.min_sum)
    await message.answer(
        default_languages[user_lang]['min_sum_prompt']
    )


@dp.message(UserHousStates.min_sum)
async def ask_max_sum(message: Message, state: FSMContext):
    user_lang = await get_user_language(message.from_user.id)
    text = default_languages[user_lang]['invalid_sum']
    try:
        min_sum = int(message.text)
    except ValueError:
        await message.answer(text=text)
        return

    await state.update_data(min_sum=min_sum)

    await state.set_state(UserHousStates.max_sum)
    await message.answer(
        default_languages[user_lang]['max_sum_prompt']
    )


@dp.message(UserHousStates.max_sum)
async def finish_registration(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = await get_user_language(message.from_user.id)
    text = default_languages[user_lang]['invalid_sum']
    try:
        max_sum = int(message.text)
    except ValueError:
        await message.answer(text=text)
        return

    await state.update_data(max_sum=max_sum)
    data = await state.get_data()

    await message.answer(
        default_languages[user_lang]['summary'].format(
            room=data['room'],
            min_sum=f"{data['min_sum']}$",
            max_sum=f"{data['max_sum']}$"
        )
    )

    state_data = await state.get_data()
    room = state_data.get('room')
    min_sum = state_data.get('min_sum')

    user_data = {
        "telegram_id": user_id,
        "room": room,
        "min_sum": min_sum,
        "max_sum": max_sum
    }
    await save_user_info_to_db_create(user_data)

    await state.clear()
