# Generated by Django 3.2.9 on 2021-11-29 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0003_alter_publication_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pubhastags',
            name='pub_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicationapp.publication', verbose_name='id публикации'),
        ),
    ]