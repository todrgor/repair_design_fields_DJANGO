# Generated by Django 3.2.9 on 2021-11-29 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(default=9998000, verbose_name='Возраст'),
        ),
    ]