# Generated by Django 2.2 on 2019-04-29 10:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('translation', '0002_auto_20190424_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='translation_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
