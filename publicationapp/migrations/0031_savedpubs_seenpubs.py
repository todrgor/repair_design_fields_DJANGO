# Generated by Django 3.2.9 on 2022-05-31 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publicationapp', '0030_auto_20220601_0303'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeenPubs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последнего просмотра публикации')),
                ('count', models.IntegerField(default=0, verbose_name='Сколько раз публикация была просмотрена')),
                ('pub', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='publicationapp.publication', verbose_name='id публикации')),
                ('watcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='id просмотревшего')),
            ],
            options={
                'verbose_name': 'Просмотренная публикация',
                'verbose_name_plural': 'Просмотренные публикации',
            },
        ),
        migrations.CreateModel(
            name='SavedPubs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время сохранения публикации')),
                ('pub', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='publicationapp.publication', verbose_name='id публикации')),
                ('saver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='id сохранившего')),
            ],
            options={
                'verbose_name': 'Сохранённая публикация',
                'verbose_name_plural': 'Сохранённые публикации',
            },
        ),
    ]