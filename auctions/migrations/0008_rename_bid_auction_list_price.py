# Generated by Django 4.2.1 on 2023-06-13 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_rename_price_auction_list_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction_list',
            old_name='bid',
            new_name='price',
        ),
    ]
