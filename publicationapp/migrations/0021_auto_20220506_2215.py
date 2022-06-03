# Generated by Django 3.2.9 on 2022-05-06 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicationapp', '0020_auto_20220426_0352'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pubtypes',
            options={'verbose_name': 'Тип публикации', 'verbose_name_plural': 'Типы публикаций'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('name',), 'verbose_name': 'Тег публикации', 'verbose_name_plural': 'Теги публикции'},
        ),
        migrations.AlterField(
            model_name='pubtypes',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='id типа'),
        ),
        migrations.AlterField(
            model_name='pubtypes',
            name='name',
            field=models.CharField(max_length=135, verbose_name='Значение типа'),
        ),
    ]