# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0019_auto_20180320_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='payment_ref',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='payments',
            name='status',
            field=models.CharField(default='Pending', max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='sub_category',
            field=models.CharField(max_length=50, null=True, choices=[(b'', b'Select Tag'), (b'men shoes', b'men shoes'), (b'bags', b'bags'), (b'beads', b'beads'), (b'belts', b'belts'), (b'women shoes', b'women shoes'), (b'jumpsuits', b'jumpsuits'), (b'watches', b'watches'), (b'slacks', b'slacks'), (b'shirts', b'shirts'), (b'menjeans', b'menjeans'), (b'womenjeans', b'womenjeans'), (b'skirts', b'skirts'), (b'dresses', b'dresses'), (b'tops', b'tops'), (b'wallets', b'wallets')]),
        ),
    ]
