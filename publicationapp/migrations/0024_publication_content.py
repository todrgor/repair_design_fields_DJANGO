# Generated by Django 3.2.9 on 2022-05-07 15:01

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0023_remove_publication_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
