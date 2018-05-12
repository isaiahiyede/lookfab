# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0021_costsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='packageID',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
