# Generated by Django 4.2 on 2024-11-11 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_house_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='room_en',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='room'),
        ),
        migrations.AddField(
            model_name='house',
            name='room_ru',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='room'),
        ),
    ]
