# Generated by Django 3.1 on 2023-07-08 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=10)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount_price', models.IntegerField(default=100)),
                ('minimum_amount', models.IntegerField(default=500)),
            ],
        ),
    ]
