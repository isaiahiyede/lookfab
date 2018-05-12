# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0013_auto_20180319_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packages',
            name='items_count',
        ),
        migrations.AddField(
            model_name='packages',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
