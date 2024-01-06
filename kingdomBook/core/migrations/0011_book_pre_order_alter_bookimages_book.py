# Generated by Django 4.2.3 on 2023-08-07 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pre_order',
            field=models.CharField(default='No', max_length=100),
        ),
        migrations.AlterField(
            model_name='bookimages',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='b_images', to='core.book'),
        ),
    ]