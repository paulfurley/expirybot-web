# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-20 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blacklist', '0003_create_new_custom_permission'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddressOwnershipProof',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner_proof', to='blacklist.EmailAddress')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_address_ownership_proofs', to='users.UserProfile')),
            ],
        ),
    ]