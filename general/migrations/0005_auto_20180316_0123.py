# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_auto_20180316_0049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='shipping_cost',
            new_name='shipping_cost_NGN',
        ),
        migrations.AddField(
            model_name='item',
            name='shipping_cost_USA',
            field=models.FloatField(default=1.0),
        ),
    ]
