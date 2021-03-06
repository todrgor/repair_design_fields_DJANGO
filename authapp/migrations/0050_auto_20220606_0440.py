# Generated by Django 3.2.9 on 2022-06-05 20:40

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0049_auto_20220604_2300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactingsupportphotos',
            options={'verbose_name': 'Фотография к обращению в поддержку', 'verbose_name_plural': 'Фотографии к обращениям в поддержку'},
        ),
        migrations.AlterModelOptions(
            name='contactingsupporttypes',
            options={'verbose_name': 'Тип обращения в поддержку', 'verbose_name_plural': 'Типы обращений в поддержку'},
        ),
        migrations.AlterModelOptions(
            name='notificationsnewtable',
            options={'verbose_name': 'Уведомление NEW', 'verbose_name_plural': 'Уведомления NEW'},
        ),
        migrations.AddField(
            model_name='notificationsnewtable',
            name='hover_text',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='Подсказка при наведении на уведомление'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notificationsnewtable',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='notifications_preview', verbose_name='Превью уведомления'),
        ),
        migrations.AlterField(
            model_name='actiontypes',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='action_types_icons', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'svg', 'gif'])], verbose_name='Иконка типа события'),
        ),
    ]
