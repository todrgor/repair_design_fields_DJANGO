# Generated by Django 3.2.9 on 2021-12-20 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0028_contactingsupport_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reported_count',
            field=models.IntegerField(default=0, verbose_name='Сколько раз на пользователя было жалоб'),
        ),
    ]
