# Generated by Django 3.2.3 on 2021-05-29 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bidder',
        ),
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listing'),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='listing',
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing'),
        ),
    ]