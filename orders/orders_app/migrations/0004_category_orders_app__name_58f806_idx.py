# Generated by Django 4.1.7 on 2023-03-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0003_alter_category_slug'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='orders_app__name_58f806_idx'),
        ),
    ]
