# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone
from django.conf import settings
import datetime
from django.utils import timezone
from django.template.defaultfilters import slugify
from general.modelchoices import *
import math

# Create your models here.


class CostSetting(models.Model):
    """ The stakeholders cost in percentage """
    dollar_exchange_rate = models.FloatField(default= 360.0)

    def __unicode__(self):
        return '%s' %(self.dollar_exchange_rate)


class UserAccount(models.Model):
    """ user details """
    user = models.OneToOneField(User, unique=True, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    profile_updated = models.BooleanField(default=False)


    class Meta:
	    verbose_name_plural = 'UserAccount'
	    ordering = ['-created_on']

    def __unicode__(self):
	    return '%s' %(self.user)

    def getItemsInCart(self):
		return self.orderitem_set.filter(ordered=False,deleted=False).count()

    def getUserPackages(self):
		return self.packages_set.filter(deleted=False).count()

    

class Item(models.Model):
	name                        = models.CharField(max_length=500, blank=True, null=True) 
	created_on                  = models.DateTimeField(default=timezone.now)
	courier_tracking_number     = models.CharField(max_length=500, blank=True, null=True)
	created_by                  = models.CharField(max_length=500, blank=True, null=True)
	description                 = models.CharField(max_length=500)
	quantity                    = models.IntegerField(default=1)
	quantity_left               = models.IntegerField(default=1)
	quantity_sold               = models.IntegerField(default=0)
	status                      = models.CharField(max_length=50, default="New")
	deleted                     = models.BooleanField(default=False)
	weight                      = models.FloatField(default= 1.0)
	link                        = models.CharField(max_length=500, null=True, blank=True)
	tag                         = models.CharField(max_length = 50, choices=CATEGORY, null=True)
	sub_category				= models.CharField(max_length = 50, choices=TAGS, null=True)
	archive                     = models.BooleanField(default=False)
	category                    = models.ForeignKey('Category' ,null=True,blank=True)
	price 						= models.IntegerField(default=1)
	slug 						= models.SlugField(max_length=500,unique=False,null=True,blank=True)
	shipping_cost_USA           = models.FloatField(default= 1.0)
	shipping_cost_NGN           = models.FloatField(default= 1.0)
	item_image_small            = models.ImageField(upload_to="item_photo", null=True, blank=True)
	item_image_big              = models.ImageField(upload_to="item_photo", null=True, blank=True)


	class Meta:
	    verbose_name_plural = 'Item'
	    ordering = ['-created_on']

	def __unicode__(self):
	    return '%s - %s - %s' %(self.name, self.category , self.price)


class Category(models.Model):
	category_name               = models.CharField(max_length=500, blank=True, null=True)
	created_on                  = models.DateTimeField(default=timezone.now)


	class Meta:
	    verbose_name_plural = 'Category'
	    ordering = ['-created_on']

	def __unicode__(self):
	    return '%s' %(self.category_name)



class Cart(models.Model):
	user_obj = models.ForeignKey(UserAccount,null=True,blank=True)
	order_placed = models.BooleanField(default=False)
	created_on = models.DateTimeField(default=timezone.now)


	class Meta:
	    verbose_name_plural = 'Cart'
	    ordering = ['-created_on']

	def __unicode__(self):
	    return '%s' %(self.user_obj.username)


class Packages(models.Model):
	tracking_number = models.CharField(max_length=50, blank=True, null=True)
	user = models.ForeignKey(UserAccount, null=True, blank=True)
	created_on = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=50, default="New")
	payment_status = models.CharField(max_length=50, default="Pending")
	shipping_status = models.CharField(max_length=50, default="Pending")
	items_count = models.IntegerField(default=1)
	deleted = models.BooleanField(default=False)
	total_amount = models.FloatField(default= 1.0)
	shipping_destination = models.CharField(max_length=500, null=True, blank=True)
	shippingCost = models.FloatField(default= 1.0)
	subTotal = models.FloatField(default= 1.0)

	class Meta:
	    verbose_name_plural = 'Packages'
	    ordering = ['-created_on']

	def __unicode__(self):
	    return '%s' %(self.user.user.username)

	def items_in_package_count(self):
		return self.orderitem_set.filter(ordered=True,deleted=False).count()

	def items_in_package(self):
		return self.orderitem_set.filter(ordered=True,deleted=False)


class PackageInvoice(models.Model):
    user            = models.ForeignKey(UserAccount, null = True)
    created_on      = models.DateTimeField(default = timezone.now)
    invoice         = models.FileField(upload_to='shipping_package_invoices/%Y/%m/%d')
    package         = models.ForeignKey(Packages, null=True, blank=True)
    
    class Meta:
        verbose_name_plural  = "Shipping Package Invoice"

    def __unicode__(self):
        return self.package.tracking_number


class OrderItem(models.Model):
	user_obj 					= models.ForeignKey(UserAccount,null=True,blank=True)
	name                        = models.CharField(max_length=500, blank=True, null=True) 
	created_on                  = models.DateTimeField(default=timezone.now)
	courier_tracking_number     = models.CharField(max_length=500, blank=True, null=True)
	created_by                  = models.CharField(max_length=500, blank=True, null=True)
	quantity                    = models.IntegerField(default=1)
	status                      = models.CharField(max_length=50, default="New")
	deleted                     = models.BooleanField(default=False)
	link                        = models.CharField(max_length=500, null=True, blank=True)
	price 						= models.FloatField(default= 1.0)
	slug 						= models.SlugField(max_length=500,unique=False,null=True,blank=True)
	ordered                     = models.BooleanField(default=False)
	item_id                     = models.IntegerField(default=1)
	shipping_cost_USA           = models.FloatField(default= 1.0)
	shipping_cost_NGN           = models.FloatField(default= 1.0)
	item_image                  = models.ImageField(upload_to="order_photo", null=True, blank=True)
	package						= models.ForeignKey(Packages, null=True, blank=True)
	

	class Meta:
	    verbose_name_plural = 'OrderItem'
	    ordering = ['-created_on']

	def __unicode__(self):
	    return '%s' %(self.name)

	def getTotal(self):
		return float(self.price * self.quantity)

	def getShippingCost(self,ship_to):
		if ship_to == "USA":
			return float(self.quantity * self.shipping_cost_USA)
		else: 
			return float(self.quantity * self.shipping_cost_NGN)


class Payments(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(max_length=15)
    status = models.CharField(max_length=50, blank=True, null=True, default="Pending")
    date_created = models.DateField(null=True, blank=True)
    payment_ref = models.CharField(max_length=50, blank=True, null=True)
    packageID = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
    	verbose_name_plural = 'Payments'
        ordering = ['-date']

    def __unicode__(self):
        return unicode(self.user)













