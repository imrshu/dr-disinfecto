# Generated by Django 2.0 on 2020-06-13 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_review_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='product_name',
        ),
    ]