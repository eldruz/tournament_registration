# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import registration.validators


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20141008_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='game',
            field=models.CharField(max_length=256, choices=[('2X', 'Super Street Fighter 2X'), ('USF4', 'Ultra Street Fighter 4'), ('3.3', 'Street Fighter III Third Strike')], verbose_name=b'Game played for this tournament.\n                               The games are chosen from a hardcoded list.', validators=[registration.validators.validate_game]),
        ),
    ]
