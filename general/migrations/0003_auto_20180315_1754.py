# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_auto_20180315_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='shipping',
            new_name='shipping_cost',
        ),
    ]
