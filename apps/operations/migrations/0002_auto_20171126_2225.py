# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-11-26 22:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermessage',
            old_name='add_tme',
            new_name='add_time',
        ),
    ]