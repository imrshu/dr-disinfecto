# Generated by Django 2.0 on 2020-06-13 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
    ]
