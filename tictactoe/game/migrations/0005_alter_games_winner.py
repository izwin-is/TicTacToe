# Generated by Django 4.0.2 on 2022-02-20 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0004_alter_waitinggame_options_games_href_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='winner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
