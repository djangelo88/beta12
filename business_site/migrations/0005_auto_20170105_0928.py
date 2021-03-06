# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-05 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_site', '0004_auto_20170102_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('description', 'website')]),
        ),
    ]
