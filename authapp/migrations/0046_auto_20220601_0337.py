# Generated by Django 3.2.9 on 2022-05-31 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0045_auto_20220601_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seenpubs',
            name='pub',
        ),
        migrations.RemoveField(
            model_name='seenpubs',
            name='watcher',
        ),
        migrations.DeleteModel(
            name='SavedPubs',
        ),
        migrations.DeleteModel(
            name='SeenPubs',
        ),
    ]