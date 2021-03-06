# Generated by Django 2.0 on 2020-06-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_success',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
