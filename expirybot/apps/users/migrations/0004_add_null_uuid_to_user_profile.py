# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-21 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171220_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='uuid',
            field=models.UUIDField(default=None, editable=False, null=True),
        ),
    ]
