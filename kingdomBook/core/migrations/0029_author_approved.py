# Generated by Django 4.2.3 on 2023-08-29 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_cartorder_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]