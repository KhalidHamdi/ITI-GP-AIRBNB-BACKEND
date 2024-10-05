# Generated by Django 5.1.1 on 2024-10-05 03:34

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_property_meta_propertyimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='image',
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
