# Generated by Django 3.2.9 on 2021-12-01 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0011_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='users_avatars/no_avatar.png', null=True, upload_to='users_avatars', verbose_name='Аватарка'),
        ),
    ]