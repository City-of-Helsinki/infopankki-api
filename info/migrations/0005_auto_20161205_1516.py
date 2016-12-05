# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-05 15:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_page_doc_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Embed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='page',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='info.MasterPage'),
        ),
        migrations.AddField(
            model_name='embed',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='embeds', to='info.Page'),
        ),
    ]
