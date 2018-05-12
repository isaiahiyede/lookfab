# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.shortcuts import render, redirect
import string, random, ast, json
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from general.views import randomNumber
from general.models import UserAccount,Category,Item,Payments,OrderItem,Packages,PackageInvoice, CostSetting, Payments




# Create your views here.
paystack_secret_key = "sk_live_c16adb6efeb7e9954ce7dcbc247a8286c7c47f35"
# paystack_secret_key = "sk_test_4cc21241bd9e08d8cdb7095fe90b6b0fcc85c3eb"  
paystack = Paystack(secret_key=paystack_secret_key)



def generate_purchaseRef():
    rand = ''.join(
             [random.choice(
                 string.ascii_letters + string.digits) for n in range(16)]) 
    return rand


def purchase_ref():
    ref = generate_purchaseRef()#+ "|%s" %obj_id
    return ref


@login_required
def mainPay(request):
	print "i got here"
	rp = request.POST
	print 'rp',rp
	email = request.user.email
	random_ref = purchase_ref()
	request.session['ref_no']= random_ref
	request.session['user']= request.user 
	amount = rp.get('paystack_amount')
	print amount
	request.session['amount'] = amount
	url = 'payments:verify_payment'
	callback_url = request.build_absolute_uri(reverse(url))
	print "callback-url", callback_url
	response = Transaction.initialize(reference=random_ref, 
	                          amount=(float(amount) * 100.0), email=request.user.email, callback_url=callback_url)
	# print 'response:', response
	data = response.get('data')
	# print "data:", data
	authorization_code=data['access_code']
	print "access_code", authorization_code
	url = data['authorization_url']
	# print 'url', url

	payment = Payments.objects.create(
		user=request.user,
		amount=amount,
		status="Pending",
		date_created=timezone.now(),
		payment_ref=random_ref)

	return redirect(url)
	    
   
def verify_payment(request):
	ref = request.session['ref_no']
	response_dict = Transaction.verify(reference=ref)
	data = response_dict.get('data')
	print 'status', data['status']

	if data['status'] == 'success':
	    status = "Approved"
	    user = request.session['user']
	    amount = request.session['amount']

	    order_items = OrderItem.objects.filter(user_obj=request.user.useraccount,ordered=False,deleted=False)
	    new_package = Packages.objects.create(user=request.user.useraccount)
	    new_package.tracking_number = randomNumber(8)
	    new_package.total_amount = request.session['total_amount']
	    new_package.shipping_destination = request.session['country']
	    new_package.shippingCost = request.session['shippingCost']
	    new_package.subTotal = request.session['subTotal']
	    new_package.payment_status = "Paid"
	    new_package.save()


	    for item in order_items:
	    
		    item.ordered = True
		    item.status = "Paid"
		    item.package = new_package
		    item.save()

		    stock_item = Item.objects.get(pk=item.item_id)
		    if stock_item.quantity <= 0:
		        stock_item.quantity = 0
		    else:
		        stock_item.quantity_left -= item.quantity
		        stock_item.quantity_sold += item.quantity
		    stock_item.save()


	    bank_record = Payments.objects.get(payment_ref=ref)
	    bank_record.status = status
	    bank_record.packageID = new_package.tracking_number
	    bank_record.save()
	    messages.success(request, "You have sucessfully paid for this package.")

	else:
		status = data['status']	
		messages.success(request, "You have not sucessfully paid for this package.")	

	del request.session['country']
	del request.session['shippingCost']
	del request.session['subTotal']
	del request.session['ref_no']
	del request.session['total_amount']

	return redirect('general:homepage')



