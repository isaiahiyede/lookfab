# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0006_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='item_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user_obj',
            field=models.ForeignKey(blank=True, to='general.UserAccount', null=True),
        ),
    ]
