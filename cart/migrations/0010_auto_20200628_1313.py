# Generated by Django 3.0.3 on 2020-06-28 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_auto_20200628_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=0, max_length=1543125),
        ),
    ]
