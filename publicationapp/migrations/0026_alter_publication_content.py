# Generated by Django 3.2.9 on 2022-05-07 23:25

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0025_auto_20220508_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True, verbose_name='Контент'),
        ),
    ]
