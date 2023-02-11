# Generated by Django 4.1.5 on 2023-01-24 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='is_friends',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user_is_being_followed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed_article_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user_is_following',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following_article_set', to=settings.AUTH_USER_MODEL),
        ),
    ]