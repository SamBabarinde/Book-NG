# Generated by Django 4.2.3 on 2023-08-10 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_bookreview_book_alter_bookreview_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='rating',
            field=models.IntegerField(choices=[(1, '⭐☆☆☆☆'), (2, '⭐⭐☆☆☆'), (3, '⭐⭐⭐☆☆'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')], default=None),
        ),
    ]
