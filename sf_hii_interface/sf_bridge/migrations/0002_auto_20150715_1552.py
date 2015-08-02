# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('sf_bridge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='api_from_sf',
            name='url_Enrrollment',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='api_from_sf',
            name='url_Question',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='api_from_sf',
            name='url_quote',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
