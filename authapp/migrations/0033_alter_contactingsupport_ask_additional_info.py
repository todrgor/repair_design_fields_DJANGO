# Generated by Django 3.2.9 on 2022-04-10 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0032_auto_20211231_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactingsupport',
            name='ask_additional_info',
            field=models.IntegerField(blank=True, max_length=99, null=True, verbose_name='Дополнительная информация к обращению'),
        ),
    ]
