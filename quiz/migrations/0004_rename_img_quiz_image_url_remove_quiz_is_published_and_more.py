# Generated by Django 4.1.5 on 2023-01-09 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0003_alter_quiz_options_alter_quiz_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='img',
            new_name='image_url',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='is_published',
        ),
        migrations.AddField(
            model_name='quiz',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
