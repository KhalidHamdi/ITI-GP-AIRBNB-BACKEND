# Generated by Django 5.1.1 on 2024-09-26 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_alter_property_image'),
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='landlord',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='useraccount.user'),
            preserve_default=False,
        ),
    ]
