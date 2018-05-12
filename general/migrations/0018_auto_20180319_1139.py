# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0017_packages_items_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='packages',
            name='shippingCost',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='packages',
            name='subTotal',
            field=models.FloatField(default=1.0),
        ),
    ]
