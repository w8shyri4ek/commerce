# Generated by Django 4.2.1 on 2023-06-13 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_bid_auction_list_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_list',
            name='bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_price', to='auctions.bid'),
        ),
        migrations.AlterField(
            model_name='auction_list',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='price_bid', to='auctions.bid'),
        ),
    ]
