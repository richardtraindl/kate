# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 16:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('count', models.SmallIntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('begin', models.DateTimeField(default=django.utils.timezone.now)),
                ('white_player', models.CharField(max_length=100)),
                ('white_player_human', models.BooleanField(default=True)),
                ('elapsed_time_white', models.IntegerField(default=0)),
                ('black_player', models.CharField(max_length=100)),
                ('black_player_human', models.BooleanField(default=True)),
                ('elapsed_time_black', models.IntegerField(default=0)),
                ('level', models.SmallIntegerField(default=1)),
                ('board', models.CharField(default='wRk;wKn;wBp;wQu;wKg;wBp;wKn;wRk;wPw;wPw;wPw;wPw;wPw;wPw;wPw;wPw;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;bPw;bPw;bPw;bPw;bPw;bPw;bPw;bPw;bRk;bKn;bBp;bQu;bKg;bBp;bKn;bRk;', max_length=256)),
                ('fifty_moves_count', models.SmallIntegerField(default=0)),
                ('wKg_x', models.SmallIntegerField(default=0)),
                ('wKg_y', models.SmallIntegerField(default=0)),
                ('bKg_x', models.SmallIntegerField(default=0)),
                ('bKg_y', models.SmallIntegerField(default=0)),
                ('wKg_first_movecnt', models.SmallIntegerField(default=0)),
                ('bKg_first_movecnt', models.SmallIntegerField(default=0)),
                ('wRk_a1_first_movecnt', models.SmallIntegerField(default=0)),
                ('wRk_h1_first_movecnt', models.SmallIntegerField(default=0)),
                ('bRk_a8_first_movecnt', models.SmallIntegerField(default=0)),
                ('bRk_h8_first_movecnt', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField()),
                ('move_type', models.PositiveSmallIntegerField(default=1)),
                ('srcx', models.PositiveSmallIntegerField()),
                ('srcy', models.PositiveSmallIntegerField()),
                ('dstx', models.PositiveSmallIntegerField()),
                ('dsty', models.PositiveSmallIntegerField()),
                ('e_p_fieldx', models.PositiveSmallIntegerField(null=True)),
                ('e_p_fieldy', models.PositiveSmallIntegerField(null=True)),
                ('captured_piece', models.PositiveSmallIntegerField(default=0)),
                ('prom_piece', models.PositiveSmallIntegerField(default=0)),
                ('fifty_moves_count', models.SmallIntegerField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kate.Match')),
            ],
        ),
        migrations.CreateModel(
            name='OpeningMove',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movecnt', models.PositiveSmallIntegerField()),
                ('src', models.CharField(max_length=2)),
                ('dst', models.CharField(max_length=2)),
                ('previous', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kate.OpeningMove')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kate.Match'),
        ),
        migrations.AlterUniqueTogether(
            name='openingmove',
            unique_together=set([('previous', 'movecnt', 'src', 'dst')]),
        ),
        migrations.AlterUniqueTogether(
            name='move',
            unique_together=set([('match', 'count')]),
        ),
    ]
