# Generated by Django 3.2.9 on 2022-05-06 14:22

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0037_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True, verbose_name='Номер телефона'),
        ),
    ]
