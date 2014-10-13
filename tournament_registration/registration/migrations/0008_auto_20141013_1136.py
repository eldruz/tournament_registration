# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_entry_tournament_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='tournament_date',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='tournament_title',
        ),
    ]
