# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import registration.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name=b'Nickname of the player')),
                ('team', models.CharField(max_length=128, verbose_name=b'Name of her team', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name=b'Tournament title.')),
                ('game', models.CharField(max_length=256, verbose_name=b'Game played for this tournament.\n                               The games are chosen from a hardcoded list.', choices=[('2X', 'Super Street Fighter 2X'), ('USF4', 'Ultra Street Fighter 4'), ('3.3', 'Street Fighter III Third Strike')])),
                ('date', models.DateField(verbose_name=b'Date of the tournament')),
                ('support', models.CharField(default='Unknown', max_length=256, verbose_name=b'Support on which the tournament will be played.')),
                ('nb_max', models.PositiveSmallIntegerField(default=32, verbose_name=b'Max number of participants.')),
                ('price', models.PositiveSmallIntegerField(default=0, verbose_name=b'Entry fee')),
                ('nb_per_team', models.PositiveSmallIntegerField(default=1, verbose_name=b'Number of players per team.')),
            ],
            options={
            },
            bases=(registration.models.ValidateOnSaveMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='tournament',
            unique_together=set([('title', 'date')]),
        ),
        migrations.AddField(
            model_name='player',
            name='registered_tournaments',
            field=models.ManyToManyField(to='registration.Tournament', through='registration.Entry'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('name', 'team')]),
        ),
        migrations.AddField(
            model_name='entry',
            name='player',
            field=models.ForeignKey(to='registration.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='tournament_id',
            field=models.ForeignKey(to='registration.Tournament'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('tournament_id', 'player')]),
        ),
    ]
