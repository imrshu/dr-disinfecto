# Generated by Django 2.0 on 2020-06-07 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
