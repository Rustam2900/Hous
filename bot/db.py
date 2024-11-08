from bot.models import User
from asgiref.sync import sync_to_async
from django.db import IntegrityError


@sync_to_async
def sync_save_user_language(user_id, user_lang):
    try:
        user, created = User.objects.get_or_create(
            telegram_id=user_id,
            defaults={'user_lang': user_lang}
        )

        if not created:
            if user.user_lang != user_lang:
                user.user_lang = user_lang
                user.save()

    except IntegrityError as e:
        print(f"IntegrityError: {e}")


async def save_user_language(user_id, user_lang):
    await sync_save_user_language(user_id, user_lang)
