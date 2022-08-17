# Generated by Django 4.1 on 2022-08-17 15:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0007_list_shared_with'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_with', to=settings.AUTH_USER_MODEL),
        ),
    ]
