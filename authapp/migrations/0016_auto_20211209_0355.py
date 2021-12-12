# Generated by Django 3.2.9 on 2021-12-08 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0015_auto_20211208_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='usersubscribes',
            name='star_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='star', to=settings.AUTH_USER_MODEL, verbose_name='id пользователя, про чьи новые публикации подписчик получает уведомления'),
        ),
    ]