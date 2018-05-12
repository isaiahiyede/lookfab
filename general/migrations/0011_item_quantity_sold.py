# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0010_item_quantity_left'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity_sold',
            field=models.IntegerField(default=1),
        ),
    ]
