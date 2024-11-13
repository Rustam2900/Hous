import re
from django.core.exceptions import ValidationError


def phone_number_validator(value):
    regex = re.compile(r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')
    if not regex.match(value):
        raise ValidationError("error")

    if len(value) > 20:
        raise ValidationError("size > 20")


def validate_us_zipcode(value):
    pattern = re.compile(r'^\d{5}(-\d{4})?$')
    if not pattern.match(value):
        raise ValidationError(
            'Noto\'g\'ri ZIP kod formati. Iltimos, to\'g\'ri formatda ZIP kodni kiriting: 12345 yoki 12345-6789.')
