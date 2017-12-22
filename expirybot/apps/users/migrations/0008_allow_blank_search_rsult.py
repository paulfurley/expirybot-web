# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-22 10:44
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_searchresultforkeysbyemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchresultforkeysbyemail',
            name='key_fingerprints',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=40), blank=True, size=None),
        ),
    ]