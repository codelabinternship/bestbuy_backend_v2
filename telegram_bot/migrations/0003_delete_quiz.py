# Generated by Django 4.2.23 on 2025-06-20 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0002_delete_telegrambotconfig_alter_bot_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Quiz',
        ),
    ]
