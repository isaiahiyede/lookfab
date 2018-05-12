# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_auto_20180315_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_image_big',
            field=models.ImageField(null=True, upload_to='item_photo', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='item_image_small',
            field=models.ImageField(null=True, upload_to='item_photo', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='sub_category',
            field=models.CharField(max_length=50, null=True, choices=[(b'', b'Select Tag'), (b'men shoes', b'men shoes'), (b'bags', b'bags'), (b'beads', b'beads'), (b'belts', b'belts'), (b'women shoes', b'women shoes'), (b'jumpsuits', b'jumpsuits'), (b'watches', b'watches'), (b'slacks', b'slacks')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='tag',
            field=models.CharField(max_length=50, null=True, choices=[(b'', b'Select Category'), (b'men', b'men'), (b'women', b'women')]),
        ),
    ]
