# Generated by Django 4.1.5 on 2023-01-23 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='is_friends',
            field=models.BooleanField(default='False'),
            preserve_default=False,
        ),
    ]
