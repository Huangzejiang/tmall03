# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-08 07:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20180608_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shop',
        ),
    ]