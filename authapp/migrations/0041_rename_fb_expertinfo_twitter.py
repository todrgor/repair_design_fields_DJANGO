# Generated by Django 3.2.9 on 2022-05-06 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0040_auto_20220507_0307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expertinfo',
            old_name='fb',
            new_name='twitter',
        ),
    ]
