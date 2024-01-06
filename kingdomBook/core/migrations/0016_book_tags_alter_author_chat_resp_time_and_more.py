# Generated by Django 4.2.3 on 2023-08-07 22:06

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('core', '0015_alter_address_options_book_return_policy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='author',
            name='chat_resp_time',
            field=models.CharField(default='state in %', max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='ship_on_time',
            field=models.CharField(default='state in %', max_length=100),
        ),
    ]
