# Generated by Django 3.2.9 on 2022-05-31 15:15

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0043_auto_20220512_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactingsupport',
            name='answered_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='made_answer', to=settings.AUTH_USER_MODEL, verbose_name='Ответ в лице поддержки от кого'),
        ),
        migrations.AlterField(
            model_name='contactingsupport',
            name='asked_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='made_question', to=settings.AUTH_USER_MODEL, verbose_name='Кто обратился в поддержку'),
        ),
        migrations.AlterField(
            model_name='expertinfo',
            name='expert_account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт эксперта'),
        ),
        migrations.AlterField(
            model_name='expertinfo',
            name='knowledge',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', max_length=5500, null=True, verbose_name='Стаж'),
        ),
        migrations.AlterField(
            model_name='expertinfo',
            name='offer',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', max_length=5500, null=True, verbose_name='Список предлагаемых услуг'),
        ),
        migrations.AlterField(
            model_name='seenpubs',
            name='when',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последнего просмотра публикации'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_entry',
            field=models.DateTimeField(auto_now=True, verbose_name='Последняя авторизация'),
        ),
        migrations.AlterField(
            model_name='user',
            name='reported_count',
            field=models.IntegerField(default=0, verbose_name='Жалоб на пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='seen_count',
            field=models.IntegerField(default=0, verbose_name='Просмотров страницы пользователя'),
        ),
        migrations.AlterField(
            model_name='usersubscribes',
            name='star',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='star', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, про чьи новые публикации подписчик получает уведомления'),
        ),
        migrations.AlterField(
            model_name='usersubscribes',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчика'),
        ),
    ]
