# Generated by Django 5.1.1 on 2024-10-07 03:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews_and_ratings', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='accuracy',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='check_in',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='cleanliness',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='communication',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='location',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='value',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
