# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='shipping',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='item',
            name='sub_category',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(default=1.0),
        ),
    ]
