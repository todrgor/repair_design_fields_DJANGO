# Generated by Django 3.2.9 on 2022-05-07 02:18

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0021_auto_20220506_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True),
        ),
    ]
