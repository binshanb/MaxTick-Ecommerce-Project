# Generated by Django 3.1 on 2023-07-03 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20230703_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='images',
            field=models.ImageField(blank=True, upload_to='images/items'),
        ),
    ]
