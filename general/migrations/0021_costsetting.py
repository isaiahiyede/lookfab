# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0020_auto_20180416_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dollar_exchange_rate', models.FloatField(default=360.0)),
            ],
        ),
    ]
