# Generated by Django 2.2 on 2019-04-11 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_auto_20190410_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('Hp', 'Hp'), ('Apple', 'Apple'), ('Dell', 'Dell'), ('Onepluse', 'Onepluse')], max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_type',
            field=models.CharField(choices=[('Electronic_product', 'Electronic_product'), ('accessories', 'accessories')], max_length=100),
        ),
    ]
