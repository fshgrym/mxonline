# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-03 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20171202_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(null=True, upload_to='teach/%Y/%m', verbose_name='\u5934\u50cf'),
        ),
    ]
