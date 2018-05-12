# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0008_auto_20180318_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='shipping_cost_NGN',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shipping_cost_USA',
            field=models.FloatField(default=1.0),
        ),
    ]
