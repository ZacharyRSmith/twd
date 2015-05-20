# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='first_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 20, 1, 13, 34, 228904), verbose_name=b'Time of first visit. #BigBrother'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 20, 1, 13, 46, 747597), verbose_name=b'Time of last visit. #BigBrother'),
            preserve_default=False,
        ),
    ]
