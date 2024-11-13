import re
from django.core.exceptions import ValidationError


def phone_number_validator(value):
    regex = re.compile(r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')
    if not regex.match(value):
        raise ValidationError("error")

    if len(value) > 20:
        raise ValidationError("size > 20")
