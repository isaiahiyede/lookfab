# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0009_auto_20180318_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity_left',
            field=models.IntegerField(default=1),
        ),
    ]
