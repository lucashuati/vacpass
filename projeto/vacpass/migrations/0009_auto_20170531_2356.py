# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-31 23:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacpass', '0008_auto_20170517_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlevencimento',
            name='avisado',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='controlevencimento',
            name='dose',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacpass.DoseVacina'),
        ),
    ]
