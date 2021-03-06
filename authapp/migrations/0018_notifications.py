# Generated by Django 3.2.9 on 2021-12-09 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0012_alter_pubhastags_tag_id'),
        ('authapp', '0017_alter_savedpubs_pub_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания уведомления')),
                ('noti_for_user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='publicationapp.publication', verbose_name='id публикации')),
                ('user_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='id сохранившего')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
    ]
