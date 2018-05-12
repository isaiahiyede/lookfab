# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_placed', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=500, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('courier_tracking_number', models.CharField(max_length=500, null=True, blank=True)),
                ('created_by', models.CharField(max_length=500, null=True, blank=True)),
                ('description', models.CharField(max_length=500)),
                ('quantity', models.IntegerField(default=1)),
                ('status', models.CharField(default='New', max_length=50)),
                ('deleted', models.BooleanField(default=False)),
                ('weight', models.CharField(max_length=250, null=True, blank=True)),
                ('link', models.CharField(max_length=500, null=True, blank=True)),
                ('tag', models.CharField(max_length=20, null=True, blank=True)),
                ('archive', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=1)),
                ('slug', models.SlugField(max_length=500, null=True, blank=True)),
                ('category', models.ForeignKey(blank=True, to='general.Category', null=True)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Item',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('courier_tracking_number', models.CharField(max_length=500, null=True, blank=True)),
                ('created_by', models.CharField(max_length=500, null=True, blank=True)),
                ('quantity', models.IntegerField(default=1)),
                ('status', models.CharField(default='New', max_length=50)),
                ('deleted', models.BooleanField(default=False)),
                ('link', models.CharField(max_length=500, null=True, blank=True)),
                ('price', models.IntegerField(default=1)),
                ('slug', models.SlugField(max_length=500, null=True, blank=True)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'OrderItem',
            },
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone_number', models.CharField(max_length=50, null=True, blank=True)),
                ('profile_updated', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'UserAccount',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='user_obj',
            field=models.ForeignKey(blank=True, to='general.UserAccount', null=True),
        ),
    ]
