# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=256, verbose_name=b'Tournament title.')),
                ('game', models.CharField(max_length=256, verbose_name=b'Game played for this tournament.\n                            The games are chosen from a hardcoded list.', choices=[('2X', 'Super Street Fighter 2X'), ('USF4', 'Ultra Street Fighter 4'), ('3.3', 'Street Fighter III Third Strike')])),
                ('date', models.DateTimeField(verbose_name=b'Date of the tournament')),
                ('support', models.CharField(max_length=256, verbose_name=b'Support on which the tournament will be played.')),
                ('nb_max', models.PositiveSmallIntegerField(verbose_name=b'Maximum number of participants.')),
                ('price', models.PositiveSmallIntegerField(verbose_name=b'Entry fee for the tournament')),
                ('nb_per_team', models.PositiveSmallIntegerField(default=1, verbose_name=b'Number of players per team.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tournament',
            unique_together=set([('title', 'date')]),
        ),
        migrations.AddField(
            model_name='entry',
            name='tournament_title',
            field=models.ForeignKey(to='registration.Tournament', to_field=b'title'),
            preserve_default=True,
        ),
    ]
