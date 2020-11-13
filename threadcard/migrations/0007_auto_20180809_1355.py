# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-08-09 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import threadcard.models


class Migration(migrations.Migration):

    dependencies = [
        ('threadcard', '0006_auto_20180809_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcover',
            name='id',
            field=models.SlugField(default=threadcard.models.get_short_code, editable=False, max_length=6, primary_key=True, serialize=False),
        ),
    ]
