# Generated by Django 3.2.9 on 2022-06-06 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0052_auto_20220606_1243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notificationsnewtable',
            options={'ordering': ('-when_happend',), 'verbose_name': 'Уведомление', 'verbose_name_plural': 'Уведомления'},
        ),
        migrations.DeleteModel(
            name='Notifications',
        ),
    ]
