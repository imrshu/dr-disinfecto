# Generated by Django 2.0 on 2020-06-13 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_review_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='customer_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]