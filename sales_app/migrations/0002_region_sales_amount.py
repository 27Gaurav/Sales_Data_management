# Generated by Django 4.2.13 on 2024-05-27 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='sales_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
