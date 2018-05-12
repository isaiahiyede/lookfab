# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0007_auto_20180318_0920'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payments',
            options={'ordering': ['-date'], 'verbose_name_plural': 'Payments'},
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item_image',
            field=models.ImageField(null=True, upload_to='order_photo', blank=True),
        ),
    ]
