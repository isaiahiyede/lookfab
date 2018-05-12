# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0012_auto_20180319_0400'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tracking_number', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default='New', max_length=50)),
                ('payment_status', models.CharField(default='Pending', max_length=50)),
                ('shipping_status', models.CharField(default='Pending', max_length=50)),
                ('items_count', models.IntegerField(default=1)),
                ('user', models.ForeignKey(blank=True, to='general.UserAccount', null=True)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Packages',
            },
        ),
        migrations.AddField(
            model_name='orderitem',
            name='package',
            field=models.ForeignKey(blank=True, to='general.Packages', null=True),
        ),
    ]
