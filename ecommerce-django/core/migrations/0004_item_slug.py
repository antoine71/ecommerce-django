# Generated by Django 4.0.5 on 2022-06-23 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_item_label_alter_item_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
    ]