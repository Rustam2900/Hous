from aiogram import Bot
from aiogram.enums import ParseMode
from bot.models import User, House
from asgiref.sync import sync_to_async
from django.conf import settings
from aiogram.client.default import DefaultBotProperties

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@sync_to_async
def get_users_and_houses():
    users = User.objects.filter(county__isnull=False)
    houses = House.objects.all()
    return users, houses


async def send_houses_to_users():
    users, houses = await get_users_and_houses()

    for user in users:
        min_sum = user.min_sum if user.min_sum else 0
        max_sum = user.max_sum if user.max_sum else float('inf')
        user_county = user.county

        relevant_houses = [house for house in houses if
                           house.county == user_county and min_sum <= house.price <= max_sum]

        if relevant_houses:
            for house in relevant_houses:
                house_details = (
                    f"ID######: {house.id}\n\n"
                    f"Title: {house.title}\n\n"
                    f"Description: {house.description}\n\n"
                    f"Zipcode: {house.zipcode}\n\n"
                    f"Room: {house.room}\n\n"
                    f"Price: ${house.price}\n\n"
                )
                await bot.send_message(chat_id=user.telegram_id, text=house_details)

    await bot.session.close()
