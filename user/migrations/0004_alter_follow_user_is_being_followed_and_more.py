# Generated by Django 4.1.5 on 2023-02-10 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_merge_20230210_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='user_is_being_followed',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='followed_article_set', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='follow',
            name='user_is_following',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='following_article_set', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
