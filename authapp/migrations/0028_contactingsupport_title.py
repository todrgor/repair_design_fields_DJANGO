# Generated by Django 3.2.9 on 2021-12-20 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0027_contactingsupport_ask_additional_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactingsupport',
            name='title',
            field=models.CharField(default='000', max_length=99, verbose_name='Заголовок события'),
        ),
    ]
