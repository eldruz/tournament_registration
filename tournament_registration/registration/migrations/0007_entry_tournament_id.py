# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20141009_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='tournament_id',
            field=models.ForeignKey(default=1, to='registration.Tournament'),
            preserve_default=False,
        ),
    ]
