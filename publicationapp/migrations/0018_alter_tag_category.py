# Generated by Django 3.2.9 on 2022-04-22 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0017_auto_20220415_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicationapp.tagcategory', verbose_name='Категория тега'),
        ),
    ]