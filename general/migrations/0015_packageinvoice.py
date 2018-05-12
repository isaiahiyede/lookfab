# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0014_auto_20180319_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageInvoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('invoice', models.FileField(upload_to='shipping_package_invoices/%Y/%m/%d')),
                ('total_amount', models.FloatField(default=1.0)),
                ('shipping_destination', models.CharField(max_length=500, null=True, blank=True)),
                ('package', models.ForeignKey(blank=True, to='general.Packages', null=True)),
                ('user', models.ForeignKey(to='general.UserAccount', null=True)),
            ],
            options={
                'verbose_name_plural': 'Shipping Package Invoice',
            },
        ),
    ]
