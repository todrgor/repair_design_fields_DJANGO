# Generated by Django 3.2.9 on 2022-06-06 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0054_rename_notificationsnewtable_notifications'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journalactions',
            options={'verbose_name': 'Одно событие', 'verbose_name_plural': 'Журнал событий'},
        ),
        migrations.AddField(
            model_name='notifications',
            name='preview',
            field=models.ImageField(blank=True, default='../../static/sources/SVG/logo_mini.svg', null=True, upload_to='notifications_preview', verbose_name='Превью уведомления'),
        ),
    ]
