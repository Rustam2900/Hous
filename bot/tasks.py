from celery import shared_task
from asgiref.sync import sync_to_async
from bot.helpers import send_houses_to_users


@shared_task
def check_for_new_houses():
    sync_to_async(send_houses_to_users)()
