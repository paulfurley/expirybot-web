# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-20 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailaddressownershipproof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='notify_email_addresses',
            field=models.BooleanField(default=True),
        ),
    ]
