# Generated by Django 3.2.9 on 2021-12-01 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0012_alter_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(verbose_name='Возраст'),
        ),
    ]