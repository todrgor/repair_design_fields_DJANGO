# Generated by Django 3.2.9 on 2021-12-20 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0026_auto_20211221_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactingsupport',
            name='ask_additional_info',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='Дополнительная информация к обращению'),
        ),
    ]
