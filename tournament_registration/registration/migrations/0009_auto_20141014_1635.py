# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_auto_20141013_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('name', models.CharField(max_length=256, serialize=False, verbose_name=b'Nickname of the player', primary_key=True)),
                ('team', models.CharField(max_length=128, verbose_name=b'Name of her team', blank=True)),
                ('registered_tournaments', models.ManyToManyField(to='registration.Tournament', through='registration.Entry')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('name', 'team')]),
        ),
        migrations.AlterField(
            model_name='entry',
            name='player',
            field=models.ForeignKey(to='registration.Player'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='nb_max',
            field=models.PositiveSmallIntegerField(default=32, verbose_name=b'Maximum number of participants.'),
        ),
    ]
