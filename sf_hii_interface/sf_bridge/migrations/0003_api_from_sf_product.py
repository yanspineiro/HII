# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('sf_bridge', '0002_auto_20150715_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='api_from_sf',
            name='product',
            field=models.CharField(default=b'', max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
