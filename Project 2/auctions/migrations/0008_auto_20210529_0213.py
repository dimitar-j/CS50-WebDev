# Generated by Django 3.2.3 on 2021-05-29 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210529_0126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='current_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='start_bid',
        ),
    ]
