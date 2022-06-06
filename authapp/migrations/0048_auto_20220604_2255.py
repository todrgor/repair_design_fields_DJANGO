# Generated by Django 3.2.9 on 2022-06-04 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0047_alter_expertinfo_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionTypes',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='id типа события')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование типа события')),
                ('icon', models.ImageField(blank=True, default='', null=True, upload_to='action_types_icons', verbose_name='Иконка типа события')),
            ],
            options={
                'verbose_name': 'Тип события',
                'verbose_name_plural': 'Типы событий',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='following_for',
            field=models.ManyToManyField(related_name='users_in_follows', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, про кого подписчик получает уведомления'),
        ),
        migrations.AlterField(
            model_name='contactingsupporttypes',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование вида обращения'),
        ),
        migrations.AlterField(
            model_name='userroles',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование роли'),
        ),
        migrations.CreateModel(
            name='NotificationsNewTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when_happend', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания уведомления')),
                ('content', models.CharField(max_length=500, verbose_name='Содержание уведомления')),
                ('url', models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка')),
                ('url_text', models.CharField(blank=True, max_length=500, null=True, verbose_name='Текст на ссылке')),
                ('receiver', models.ManyToManyField(related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='Получатели уведомления')),
                ('receiver_saw', models.ManyToManyField(related_name='receiver_saw', to=settings.AUTH_USER_MODEL, verbose_name='Просмотревшие уведомление')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authapp.actiontypes', verbose_name='Тип события')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
        migrations.CreateModel(
            name='JournalActions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время события')),
                ('action_content', models.CharField(max_length=1500, verbose_name='Содержание события')),
                ('action_subjects_list', models.CharField(max_length=500, verbose_name='Список объектов, попавших в событие')),
                ('action_person', models.ManyToManyField(null=True, related_name='person', to=settings.AUTH_USER_MODEL, verbose_name='Действующее лицо')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authapp.actiontypes', verbose_name='Тип события')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
            },
        ),
    ]
