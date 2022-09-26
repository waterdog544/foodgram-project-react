# Generated by Django 3.2.15 on 2022-09-26 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(help_text='Цвет в HEX', max_length=16, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(help_text='Уникальный слаг', max_length=16, verbose_name='URl-aдрес'),
        ),
    ]