# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-13 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PGPKey',
            fields=[
                ('fingerprint', models.CharField(help_text='The 40-character key fingerprint without spaces.', max_length=40, primary_key=True, serialize=False)),
                ('key_algorithm', models.CharField(choices=[('DSA (1)', 'DSA'), ('RSA (17)', 'RSA'), ('ECC (18)', 'ECC'), ('ECDSA (19)', 'ECDSA')], max_length=10)),
                ('key_length_bits', models.PositiveSmallIntegerField()),
                ('last_synced', models.DateTimeField(blank=True, null=True)),
                ('creation_datetime', models.DateTimeField(blank=True, null=True)),
                ('expiry_datetime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UID',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('uid_string', models.CharField(max_length=500)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uids', to='keys.PGPKey')),
            ],
        ),
    ]
