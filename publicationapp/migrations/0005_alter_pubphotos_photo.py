# Generated by Django 3.2.9 on 2021-11-29 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0004_alter_pubhastags_pub_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pubphotos',
            name='photo',
            field=models.ImageField(max_length=200, upload_to='pub_media', verbose_name='Фотографии публикации'),
        ),
    ]
