import os

from celery import shared_task
from asgiref.sync import sync_to_async
from django.conf import settings
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.models import User, House

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@shared_task
def check_for_new_houses():
    users = User.objects.filter(county__isnull=False)

    for user in users:
        min_sum = user.min_sum if user.min_sum else 0
        max_sum = user.max_sum if user.max_sum else float('inf')
        user_county = user.county

        houses = House.objects.filter(
            county=user_county,
            price__gte=min_sum,
            price__lte=max_sum
        )

        if houses:
            for house in houses:
                house_details = (f"ID######: {house.id} \n\n"
                                 f"Title: {house.title}\n\n"
                                 f"Description: {house.description}\n\n"
                                 f"Zipcode: {house.zipcode}\n\n"
                                 f"Room: {house.room}\n\n"
                                 f"Price: ${house.price}\n\n")
                sync_to_async(bot.send_message)(
                    chat_id=user.telegram_id,
                    text=house_details
                )


bot.close()
