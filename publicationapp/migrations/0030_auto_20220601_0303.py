# Generated by Django 3.2.9 on 2022-05-31 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0029_auto_20220601_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='average_age_savers',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='average_age_watchers',
        ),
    ]
