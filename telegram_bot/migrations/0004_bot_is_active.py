# Generated by Django 4.2.23 on 2025-06-24 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0003_delete_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
