# Generated by Django 3.2.3 on 2021-05-30 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210529_0213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='price',
            new_name='current_price',
        ),
        migrations.AddField(
            model_name='listing',
            name='start_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=64),
        ),
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
