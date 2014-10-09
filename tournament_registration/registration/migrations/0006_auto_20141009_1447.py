# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20141008_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='tournament_date',
            field=models.DateField(default=datetime.date(2014, 10, 9), verbose_name=b'Date of the tournament'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='tournament_title',
            field=models.CharField(max_length=256, verbose_name=b'Tournament title'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='title',
            field=models.CharField(max_length=256, verbose_name=b'Tournament title.'),
        ),
    ]
