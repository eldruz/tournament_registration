# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_prices.models
import satchless.item


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_remove_tournament_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', django_prices.models.PriceField(default=0.0, currency=b'EUR', verbose_name=b'Price', max_digits=5, decimal_places=2)),
                ('date_added', models.DateField(verbose_name=b'Date added')),
                ('last_modified', models.DateTimeField(verbose_name=b'Last modified')),
                ('tournament', models.OneToOneField(to='registration.Tournament')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, satchless.item.StockedItem),
        ),
    ]
