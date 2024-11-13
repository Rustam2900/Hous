# Generated by Django 4.2 on 2024-11-13 10:10

import bot.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0017_alter_house_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='zipcode',
            field=models.CharField(blank=True, null=True, validators=[bot.validators.validate_us_zipcode]),
        ),
    ]
