# Generated by Django 4.2.23 on 2025-06-24 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0005_alter_bot_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
