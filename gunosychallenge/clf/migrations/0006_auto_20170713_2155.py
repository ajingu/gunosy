# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clf', '0005_auto_20170713_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(max_length=100),
        ),
    ]
