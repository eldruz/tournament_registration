# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='price',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'Entry fee for the tournament'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='support',
            field=models.CharField(default='Unknown', max_length=256, verbose_name=b'Support on which the tournament will be played.'),
        ),
    ]
