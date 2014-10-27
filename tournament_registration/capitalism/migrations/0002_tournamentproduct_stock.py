# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capitalism', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentproduct',
            name='stock',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'Product Stock'),
            preserve_default=True,
        ),
    ]
