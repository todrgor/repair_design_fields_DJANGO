# Generated by Django 3.2.9 on 2022-04-22 15:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0018_alter_tag_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='cost_max',
            field=models.FloatField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='бюджет до'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='cost_min',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='бюджет от'),
        ),
    ]