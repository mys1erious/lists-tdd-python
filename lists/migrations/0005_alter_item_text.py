# Generated by Django 4.1 on 2022-08-11 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_alter_item_options_alter_item_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
