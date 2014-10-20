# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_tournament_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='slug',
            field=models.SlugField(default=b'2014-10-20', max_length=256, verbose_name=b'Player slug'),
            preserve_default=False,
        ),
    ]
