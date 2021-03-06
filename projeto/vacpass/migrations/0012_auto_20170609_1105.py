# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-09 11:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacpass', '0011_auto_20170604_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlevencimento',
            name='dose',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacpass.DoseVacina'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='vacina',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacpass.Vacina', to_field='nome'),
        ),
        migrations.AlterField(
            model_name='vacina',
            name='nome',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
