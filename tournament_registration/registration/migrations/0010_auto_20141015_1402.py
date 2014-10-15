# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_auto_20141014_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='nb_max',
            field=models.PositiveSmallIntegerField(default=32, verbose_name=b'Max number of participants.'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='price',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'Entry fee'),
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('tournament_id', 'player')]),
        ),
    ]
