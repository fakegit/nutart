# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-13 15:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutcms', '0004_movieresource'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Entry',
        ),
        migrations.RenameModel(
            old_name='PostMeta',
            new_name='EntryMeta',
        ),
    ]
