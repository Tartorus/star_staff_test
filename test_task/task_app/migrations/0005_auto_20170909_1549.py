# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-09 15:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0004_auto_20170909_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_body',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_published_time',
            new_name='published_time',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_title',
            new_name='title',
        ),
    ]
