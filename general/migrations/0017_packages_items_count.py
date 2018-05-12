# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0016_auto_20180319_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='packages',
            name='items_count',
            field=models.IntegerField(default=1),
        ),
    ]
