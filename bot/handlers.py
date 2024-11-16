import re

from aiogram.client.default import DefaultBotProperties
from django.conf import settings
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram import Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from telegraph import Telegraph

from bot.keyboards import get_languages, get_main_menu
from bot.models import User, House, HouseMeasure, HouseImage
from bot.utils import default_languages, introduction_template
from bot.db import (save_user_language, save_user_info_to_db,
                    get_user_language, state_get, county_get, create_or_update_user_state,
                    create_or_update_user_country, save_user_info_to_db_create, get_house_image)
from bot.utils import user_languages
from bot.states import UserStates, UserHousStates

from bot.validators import validate_us_zipcode

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

dp = Dispatcher()
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

phone_number_validator = re.compile(r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')

telegraph = Telegraph()
telegraph.create_account(short_name='SamItGlobalHousBot')  # o'zingizning bot nomingizni kiriting


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
        phone = message.contact.phone_number
    else:
        phone = message.text.strip()

    if not phone_number_validator.match(phone):
        error_message = default_languages[user_lang].get("enter_number", "Please enter a valid phone number.")
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
    await call.message.edit_reply_markup(default_languages[user_lang]['state_'], reply_markup=inline_kb)


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
    await call.message.edit_reply_markup(default_languages[user_lang]['country'], reply_markup=inline_kb)
    user, created = await create_or_update_user_state(
        telegram_id=user_id,
        state_id=state_id
    )


@dp.callback_query(lambda call: call.data.startswith("country_"))
async def handle_county_selection(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_lang = await get_user_language(user_id)

    county_id = int(call.data.split("_")[1])
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

    await state.set_state(UserHousStates.zipcode)
    await message.answer(
        default_languages[user_lang]['zipcode']
    )


@dp.message(UserHousStates.zipcode)
async def ask_max_sum(message: Message, state: FSMContext):
    user_lang = await get_user_language(message.from_user.id)
    text = default_languages[user_lang]['room_prompt']
    zipcode = message.text.strip()

    try:
        validate_us_zipcode(zipcode)
    except ValidationError as e:
        await message.answer(str(e))
        return

    await state.update_data(zipcode=zipcode)

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
    inline_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[])
    inline_buttons = []
    inline_buttons.append(
        InlineKeyboardButton(text=default_languages[user_lang]['filter'] or "no name",
                             callback_data="filter_"))

    inline_kb.inline_keyboard = [inline_buttons[i:i + 1] for i in range(0, len(inline_buttons), 1)]
    await message.answer(
        default_languages[user_lang]['summary'].format(
            room=data['room'],
            zipcode=data['zipcode'],
            min_sum=f"{data['min_sum']}$",
            max_sum=f"{data['max_sum']}$"
        ),
        reply_markup=inline_kb
    )

    state_data = await state.get_data()
    room = state_data.get('room')
    zipcode = state_data.get('zipcode')
    min_sum = state_data.get('min_sum')

    user_data = {
        "telegram_id": user_id,
        "room": room,
        "zipcode": zipcode,
        "min_sum": min_sum,
        "max_sum": max_sum
    }
    await save_user_info_to_db_create(user_data)

    await state.clear()


@dp.callback_query(lambda call: call.data.startswith("filter_"))
async def handle_county_selection(call: CallbackQuery):
    user_id = call.from_user.id
    user_lang = await get_user_language(user_id)

    try:
        user = await sync_to_async(User.objects.get)(telegram_id=user_id)
    except User.DoesNotExist:
        await call.message.answer(default_languages[user_lang]['user_not'])
        return

    user_county = await sync_to_async(lambda: user.county)()

    if not user_county:
        await call.message.answer(default_languages[user_lang]['county_user_update'])
        return

    min_sum = user.min_sum if user.min_sum else 0
    max_sum = user.max_sum if user.max_sum else float('inf')

    houses = await sync_to_async(lambda: list(House.objects.filter(
        county=user_county,
        price__gte=min_sum,
        price__lte=max_sum
    )))()

    if houses:
        for house in houses:
            house_details = (f"ID######: {house.id} \n\n"
                             f"Title: {house.title}\n\n"
                             f"Description: {house.description}\n\n"
                             f"Zipcode: {house.zipcode}\n\n"
                             f"Room: {house.room}\n\n"
                             f"Price: ${house.price}\n\n")

            inline_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[])

            inline_buttons = [
                InlineKeyboardButton(
                    text=default_languages[user_lang]['details'] or "no name",
                    callback_data=f"details_{house.id}"
                )
            ]
            inline_kb.inline_keyboard = [inline_buttons[i:i + 1] for i in range(0, len(inline_buttons), 1)]

            await call.message.answer(house_details, reply_markup=inline_kb)
    else:
        await call.message.answer(default_languages[user_lang]['county_user_not'])


@dp.callback_query(lambda call: call.data.startswith("details_"))
async def show_house_details(call: CallbackQuery):
    user_id = call.from_user.id
    user_lang = await get_user_language(user_id)

    callback_data = call.data.split("_")

    if len(callback_data) < 2 or not callback_data[1].isdigit():
        await call.message.answer(default_languages[user_lang]['not'])
        return

    house_id = int(callback_data[1])

    try:
        house = await sync_to_async(House.objects.get)(id=house_id)
        house_measure = await sync_to_async(HouseMeasure.objects.get)(house=house)
        print("@@@@@@@@##########", house_measure)
        house_images_query = await get_house_image(house=house_id)

        print("############", list(house_images_query))
        house_details = (
            f"🏠 <b>{house.title}</b>\n\n"
            f"📜 {house.description}\n"
            f"📍 {default_languages[user_lang]['zipcode']}: {house.zipcode}\n"
            f"🚪 {default_languages[user_lang]['room']}: {house.room}\n"
            f"💵 {default_languages[user_lang]['price']}: ${house.price}\n\n"
            f"{default_languages[user_lang]['details']}\n"
            f"{default_languages[user_lang]['living_room_area']}: {house_measure.living_room_area} m²\n"
            f"{default_languages[user_lang]['bedroom_area']}: {house_measure.bedroom_area} m²\n"
            f"{default_languages[user_lang]['number_of_toilets']}: {house_measure.bathroom_count}\n"
            f"{default_languages[user_lang]['kitchen_area']}: {house_measure.kitchen_area} m²\n"
            f"{default_languages[user_lang]['year_built']}: {house_measure.year_built}\n"
            f"{default_languages[user_lang]['total_area']}: {house_measure.total_area} m²\n"
        )

        for image in house_images_query:
            image_url = f"{settings.MEDIA_URL}{image.image}"
            await call.message.answer_photo(photo=image_url, caption=f"{house.title}")
        # print("###################", image_url)
        telegraph_content = f"""
            <strong>Description:</strong><br>{house.description}<br>
            <strong>Details:</strong><br>
            <ul>
                <li><strong>Zipcode:</strong> {house.zipcode}</li>
                <li><strong>Room:</strong> {house.room}</li>
                <li><strong>Price:</strong> ${house.price}</li>
                <li><strong>Living Room Area:</strong> {house_measure.living_room_area} m²</li>
                <li><strong>Bedroom Area:</strong> {house_measure.bedroom_area} m²</li>
                <li><strong>Bathroom Count:</strong> {house_measure.bathroom_count}</li>
                <li><strong>Kitchen Area:</strong> {house_measure.kitchen_area} m²</li>
                <li><strong>Year Built:</strong> {house_measure.year_built}</li>
                <li><strong>Total Area:</strong> {house_measure.total_area} m²</li>
            </ul>
        """

        telegraph_response = telegraph.create_page(
            title=f"{house.title} - Details",
            html_content=telegraph_content,
            author_name="Rustam",
            author_url="https://t.me/Jumanazarov_Rustam"
        )

        house_details += f"\n🔗 {default_languages[user_lang]['more']}: https://telegra.ph/{telegraph_response['path']}"

        await call.message.answer(house_details, parse_mode="HTML")

    except House.DoesNotExist:
        await call.message.answer(default_languages[user_lang]['house_not'])
    except HouseMeasure.DoesNotExist:
        await call.message.answer(default_languages[user_lang]['measure_not'])
    except Exception as e:
        print(f"Error: {e}")
        await call.message.answer('error')
