# Generated by Django 4.2.2 on 2023-07-28 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bakery', '0003_product_type_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_type',
            name='id',
        ),
    ]
