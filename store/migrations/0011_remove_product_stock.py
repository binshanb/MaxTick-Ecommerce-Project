# Generated by Django 3.1 on 2023-07-20 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_watch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]
