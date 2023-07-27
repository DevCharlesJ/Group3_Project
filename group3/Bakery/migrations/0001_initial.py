# Generated by Django 4.2.2 on 2023-07-27 17:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='customer_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customer_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=350, null=True)),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
        ),
        migrations.CreateModel(
            name='Product_Type',
            fields=[
                ('name', models.CharField(max_length=80, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Shopping_Cart',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('customer', models.OneToOneField(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='Bakery.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Shopping_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='Bakery.product')),
                ('shopping_cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='Bakery.shopping_cart')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Bakery.product_type'),
        ),
        migrations.AddConstraint(
            model_name='shopping_item',
            constraint=models.UniqueConstraint(fields=('shopping_cart', 'product'), name='unique_shopping_cart_product_combination'),
        ),
    ]
