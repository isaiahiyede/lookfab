# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0018_auto_20180319_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='weight',
            field=models.FloatField(default=1.0),
        ),
    ]
