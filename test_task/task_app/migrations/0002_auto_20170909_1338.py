# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-09 13:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 9, 13, 38, 13, 937362, tzinfo=utc)),
        ),
    ]
