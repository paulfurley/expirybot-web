# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-26 12:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0023_add_custom_permission_to_key_upate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keyupdate',
            options={'ordering': ('-updated_at',), 'permissions': (('add_key_update', 'Can create key KeyUpdate records.'),)},
        ),
    ]
