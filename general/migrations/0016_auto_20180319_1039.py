# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0015_packageinvoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packageinvoice',
            name='shipping_destination',
        ),
        migrations.RemoveField(
            model_name='packageinvoice',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='packages',
            name='shipping_destination',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='packages',
            name='total_amount',
            field=models.FloatField(default=1.0),
        ),
    ]
