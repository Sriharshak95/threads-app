# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-07-09 07:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookcover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('tagline', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.CharField(blank=True, max_length=512)),
                ('url', models.URLField(blank=True, null=True)),
                ('live', models.BooleanField(default=True)),
                ('thread_count', models.IntegerField(default=0)),
                ('rating_count', models.IntegerField(default=0)),
                ('rating_sum', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='thredcards')),
            ],
            options={
                'db_table': 'Bookcover',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('comment', models.CharField(max_length=200, null=True)),
                ('like', models.BooleanField(default=False)),
                ('bookcover', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='threadcard.Bookcover')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Rating',
            },
        ),
        migrations.CreateModel(
            name='SubComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('comment', models.CharField(max_length=200)),
                ('live', models.BooleanField(default=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='subcomment')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SubComment',
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('message', models.CharField(max_length=500)),
                ('live', models.BooleanField(default=True)),
                ('subcomment_count', models.IntegerField(default=0)),
                ('image', models.FileField(blank=True, null=True, upload_to='threads')),
                ('bookcover', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='threadcard.Bookcover')),
                ('bookcoverowner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Thread',
            },
        ),
        migrations.CreateModel(
            name='TwitterUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image_url', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='twitter_profiles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subcomment',
            name='threadname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='threadcard.Thread'),
        ),
        migrations.AddField(
            model_name='bookcover',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='threadcard.Category'),
        ),
        migrations.AddField(
            model_name='bookcover',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]