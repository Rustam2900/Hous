from bot.models import User, State, County
from asgiref.sync import sync_to_async
from django.db import IntegrityError


@sync_to_async
def get_user_language(user_id):
    try:
        user = User.objects.get(telegram_id=user_id)
        return user.user_lang
    except User.DoesNotExist:
        return 'en'


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


@sync_to_async
def save_user_info_to_db(user_data):
    try:
        new_user, created = User.objects.update_or_create(
            telegram_id=user_data['telegram_id'],
            defaults={
                "full_name": user_data['full_name'],
                "phone_number": user_data['phone_number'],
                "tg_username": user_data['tg_username'],
                "username": user_data['username']
            }
        )
        return new_user
    except IntegrityError:
        raise Exception("User already exists")


@sync_to_async
def save_user_info_to_db_create(user_data):
    try:
        new_user, created = User.objects.update_or_create(
            telegram_id=user_data['telegram_id'],
            defaults={
                "room": user_data['room'],
                "zipcode": user_data['zipcode'],
                "min_sum": user_data['min_sum'],
                "max_sum": user_data['max_sum']
            }
        )
        return new_user
    except IntegrityError:
        raise Exception("User already exists")


@sync_to_async
def state_get():
    return list(State.objects.all())


@sync_to_async
def county_get(state_id):
    return list(County.objects.filter(state_id=state_id))


@sync_to_async
def create_or_update_user_state(telegram_id, state_id):
    try:
        state_instance = State.objects.get(id=state_id)

        user, created = User.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={
                'state': state_instance
            }
        )
        return user, created
    except (IntegrityError, State.DoesNotExist) as e:
        return None, False


@sync_to_async
def create_or_update_user_country(telegram_id, county_id):
    try:
        county_instance = County.objects.get(id=county_id)

        state_instance = county_instance.state

        user, created = User.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={
                'state': state_instance,
                'county': county_instance,
            }
        )
        return user, created
    except (IntegrityError, County.DoesNotExist) as e:
        return None, False


def fix_phone(phone):
    if "+" not in phone:
        return f"+{phone}"
    return phone
