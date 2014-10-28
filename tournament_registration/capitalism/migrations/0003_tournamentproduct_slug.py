# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capitalism', '0002_tournamentproduct_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentproduct',
            name='slug',
            field=models.SlugField(default='Pataprout', max_length=256, verbose_name=b'Product slug'),
            preserve_default=False,
        ),
    ]
