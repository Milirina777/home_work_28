# Generated by Django 4.1.7 on 2023-02-18 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0009_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ads',
            options={'ordering': ['name'], 'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
    ]
