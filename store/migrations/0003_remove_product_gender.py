# Generated by Django 3.1 on 2023-07-01 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20230701_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='gender',
        ),
    ]
