# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 14:54
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20171113_1543'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='transaction',
            managers=[
                ('activetransactions', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='actif',
            new_name='active',
        ),
    ]
