# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-03 02:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20170102_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='default_site_mine',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='business',
            name='websiteurl',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 2, 21, 30, 43, 422424)),
        ),
    ]
