# Generated by Django 3.2.3 on 2021-06-01 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210530_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='current_price',
        ),
    ]
