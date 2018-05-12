from __future__ import unicode_literals
from django.template.loader import render_to_string, get_template
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from general.forms import UserForm, CategoryForm, ItemForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.template.defaultfilters import slugify
from django.template.context import RequestContext
from django.template import Context
from django.db.models import Count
from django import template
import random, datetime, string
from django.core.urlresolvers import reverse
import json
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.db.models import Sum, Max
from django.utils import timezone
from general.models import UserAccount,Category,Item,Payments,OrderItem,Packages,PackageInvoice, CostSetting
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum
import csv


# start helper functions here

def random_no(value):
    allowed_chars = ''.join((string.digits))
    unique_id = ''.join(random.choice(allowed_chars) for _ in range(5))
    while Item.objects.filter(courier_tracking_number=unique_id):
        unique_id = ''.join(random.choice(allowed_chars) for _ in range(5))
    return unique_id


def randomNumber(value):
    allowed_chars = ''.join((string.digits))
    unique_id = ''.join(random.choice(allowed_chars) for _ in range(5))
    while Packages.objects.filter(tracking_number=unique_id):
        unique_id = ''.join(random.choice(allowed_chars) for _ in range(5))
    return '#' + 'PKG' + unique_id


def paginate_list(request, objects_list, num_per_page):
    paginator = Paginator(objects_list, num_per_page)  # show number of jobs per page
    page = request.GET.get('page')
    try:
        paginated_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        paginated_list = paginator.page(1)
    except  EmptyPage:
        # if page is out of range(e.g 9999), deliver last page of results
        paginated_list = paginator.page(paginator.num_pages)
    return paginated_list

# end helper function here


# start general functions here

def homepage(request):
    context = {}
    template_name = 'general/index.html'
    userForm = UserForm()
    items = Item.objects.filter(deleted=False)
    # for item in items:
    #     item.item_image_big = ""
    #     item.item_image_small = ""
    #     item.save()
    try:
        items_in_cart = UserAccount.objects.get(user=request.user).getItemsInCart()
        context['items_in_cart'] = items_in_cart
    except:
        pass


    context['all_bags'] = items.filter(sub_category="bags")[0:8]
    context['all_shoes'] = items.filter(Q(sub_category="women shoes") | Q(sub_category="men shoes"))[0:8]
    context['women_items'] = items.filter(category__category_name="women")[0:8]
    context['men_items'] = items.filter(category__category_name="men")[0:8]
    context['userForm'] = userForm
    return render(request, template_name, context)


def itemDetails(request,slug,pk):
    context = {}
    template_name = 'general/single.html'
    item = Item.objects.get(pk=pk)
    try:
        items_in_cart = UserAccount.objects.get(user=request.user).getItemsInCart()
        context['items_in_cart'] = items_in_cart
    except:
        pass
    
    context['item'] = item
    return render(request,template_name,context)


def storeItems(request,category,subcategory):
    context = {}
    template_name = 'general/sameCategoryItems.html'
    items = Item.objects.filter(category__category_name=category,sub_category=subcategory,deleted=False)
    try:
        items_in_cart = UserAccount.objects.get(user=request.user).getItemsInCart()
        context['items_in_cart'] = items_in_cart
    except:
        pass
    
    context['items'] = paginate_list(request,items,12)
    itemsPresent = True
    if(len(items)) == 0:
        itemsPresent = False
    context['itemsPresent'] = itemsPresent
    return render(request,template_name,context)


def allStoreItems(request,category):
    context = {}
    template_name = 'general/sameCategoryItems.html'
    items = Item.objects.filter(category__category_name=category,deleted=False)
    try:
        items_in_cart = UserAccount.objects.get(user=request.user).getItemsInCart()
        context['items_in_cart'] = items_in_cart
    except:
        pass
    
    context['items'] = paginate_list(request,items,12)
    itemsPresent = True
    if(len(items)) == 0:
        itemsPresent = False
    context['itemsPresent'] = itemsPresent
    return render(request,template_name,context)


def package_invoice_page(request, tracking_id):
    template = "general/package_invoice_email_template.html"
    context = {}
    pkg = get_object_or_404(Packages, tracking_number=tracking_id)
    context.update({'pkg':pkg})
    return render(request, template, context)


def user_login(request):
    # print len(eventz_all)
    if request.method == "POST":

        # print request.POST
        if request.POST.get('bot_catcher') != "":
            return redirect(reverse('general:homepage'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            username = User.objects.get(email=username).username
            # print username
        except Exception as e:
            print "e", e
            try:
                username = User.objects.get(username=username).username
                print username
                username = username
            except Exception as e:
                messages.warning(request, "Invalid login details supplied")
                return render(request, 'general/index.html', {'username': username})
        user = authenticate(username=username, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:

                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                # print "I got here"
                # try:
                #     useraccount = request.user.useraccount
                # except:
                #     return redirect(reverse('general:profile'))

                if user.is_staff:
                    return redirect(reverse('general:admin'))
                else:
                    # print request.session.keys()
                    return redirect(reverse('general:homepage'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            messages.warning(request, "Invalid login details supplied")
            return redirect(reverse('general:homepage'))

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'general/index.html',{})


@login_required
def customer_packages(request):
    context = {}
    orders_count = ""
    template_name = 'general/all_customer_packages.html'
    order_items = Packages.objects.filter(user=request.user.useraccount,deleted=False)
    if order_items:
        orders_count = True
    else:
        orders_count = False
    try:
        items_in_cart = UserAccount.objects.get(user=request.user).getItemsInCart()
        context['items_in_cart'] = items_in_cart
    except:
        pass
    context['order_items'] = paginate_list(request,order_items,12)
    context['orders_count'] = orders_count
    return render(request,template_name,context)


@login_required
def customer_orders(request):
    context = {}
    orders_count = ""
    template_name = 'general/all_customer_orders.html'
    order_items = OrderItem.objects.filter(user_obj=request.user.useraccount,deleted=False)
    if order_items:
        orders_count = True
    else:
        orders_count = False
    try:
        items_in_cart = UserAccount.objects.get(user=request.user).getItemsInCart()
        context['items_in_cart'] = items_in_cart
    except:
        pass
    context['order_items'] = paginate_list(request,order_items,12)
    context['orders_count'] = orders_count
    return render(request,template_name,context)


@login_required
def customer_payments(request):
    context = {}
    template_name = 'general/all_customer_payments.html'
    payment_list = Payments.objects.filter(user=request.user)
    try:
        items_in_cart = UserAccount.objects.get(user=request.user).getItemsInCart()
        context['items_in_cart'] = items_in_cart
    except:
        pass
    context['payment_list'] = paginate_list(request,payment_list,12)
    return render(request,template_name,context)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    if request.user.is_staff:
        response = redirect(reverse('general:homepage'))
    else:
        response = redirect(reverse('general:homepage'))

    logout(request)

    return response


@csrf_exempt
@login_required
def cart_box(request):
    print "here "
    context = {}
    template_name = "general/cartBox.html"

    out_of_stock = ""

    try:
        items_in_cart = UserAccount.objects.get(user=request.user).getItemsInCart()
        print items_in_cart
    except:
        pass

    if not request.user.is_authenticated:
        messages.warning(request,"Please login or sign up before shopping")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    the_item = Item.objects.get(pk=request.POST.get('item_pk'))

    if the_item.quantity == 0:
        context['items_in_cart'] = items_in_cart
        out_of_stock = True
        context['out_of_stock'] = out_of_stock
        return render(request,template_name,context)

    if OrderItem.objects.filter(user_obj=request.user.useraccount,item_id=the_item.pk,ordered=False,deleted=False).exists():
        order_item = OrderItem.objects.get(user_obj=request.user.useraccount,item_id=the_item.pk,ordered=False,deleted=False)
        
        order_item.quantity += 1
        if order_item.quantity > the_item.quantity:
            out_of_stock = True
            context['out_of_stock'] = out_of_stock
            context['items_in_cart'] = items_in_cart
            return JsonResponse({'out_of_stock':out_of_stock,'items_in_cart':items_in_cart})
        else:           
            order_item.save()

        
        
    else:
        print "i got here"
        OrderItem.objects.create(
            user_obj=request.user.useraccount,
            name=the_item.name,
            courier_tracking_number=the_item.courier_tracking_number,
            created_by=request.user.username,
            quantity=1,
            item_image=the_item.item_image_big,
            price=the_item.price,
            item_id=the_item.pk,
            shipping_cost_USA=the_item.shipping_cost_USA,
            shipping_cost_NGN=the_item.shipping_cost_NGN)

        items_in_cart+=1
        context['items_in_cart'] = items_in_cart

    out_of_stock = False
    context['out_of_stock'] = out_of_stock
        
    return render(request,template_name,context)


def look_fab_sendmail(request, user, title, text, pkg=None):
    name       = request.user.username
    to         = [request.user.email]
    from_email = "info@look-fab.com"
    subject = title
    msg_text = render_to_string(text)
    ctx  = {
        'username': name,
        'body': get_template(text).render(Context({'request':request})),
        'request':request,
        }
    if not pkg == None:
        ctx['body'] = get_template(text).render(Context({'pkg':pkg, 'request':request}))
    message = get_template('general/base_email.html').render(Context(ctx))
    msg = EmailMessage(subject, message, from_email, to)
    msg.content_subtype = 'html'
    msg.send()
    return HttpResponse(message)


@csrf_exempt
@login_required
def get_confirmation_order(request):
    context = {}
    template_name = 'general/orderConfirmation.html'
    ship_to = request.GET.get('item_number')
    if ship_to == 1:
        country = "USA"
    else:
        country = "Nigeria"
    request.session['country'] = country
    order_items = OrderItem.objects.filter(user_obj=request.user.useraccount,ordered=False,deleted=False)
    subTotal = 0
    shippingCost = 0
    grandTotal = 0
    for order in order_items:
        subTotal += order.getTotal()
        shippingCost += order.getShippingCost(country)

    grandTotal = subTotal + shippingCost + (0.025 * subTotal)
    try:
        cost_setting = CostSetting.objects.get(pk=1)
    except:
        cost_setting = 362.0

    total_amount = subTotal + shippingCost + (0.025 * subTotal)
    paystack_amount = (total_amount) * cost_setting

    form = PayPalPaymentsForm()

    context['grandTotal'] = grandTotal
    context['shippingCost'] = shippingCost
    context['subTotal'] = subTotal
    context['paystack_amount'] = paystack_amount
    context['total_amount'] = total_amount

    request.session['grandTotal'] = grandTotal
    request.session['shippingCost'] = shippingCost
    request.session['subTotal'] = subTotal
    request.session['total_amount'] = total_amount

    context['form'] = form

    return render(request,template_name,context)


@login_required
def view_cart(request):
    context = {}
    total = 0
    template_name = "general/checkout.html"
    order_items = OrderItem.objects.filter(user_obj=request.user.useraccount,ordered=False,deleted=False)
    for items in order_items:
        total += items.getTotal()
    context['total'] = total
    context['order_items'] = paginate_list(request,order_items,12)
    items_in_cart = UserAccount.objects.get(user=request.user).getItemsInCart()
    context['items_in_cart'] = items_in_cart
    return render(request,template_name,context)


@login_required
def remove_from_cart(request,item_pk):
    order_item = OrderItem.objects.get(user_obj=request.user.useraccount,ordered=False,pk=item_pk)
    order_item.deleted=True
    order_item.save()
    messages.warning(request, "Item has been deleted from your cart")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def register(request):
    if request.method == "POST":
        if request.POST.get('bot_catcher') != "":
            messages.warning(request, "Invalid details provided")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if request.POST.get('phone_number') == "":
            messages.warning(request, "Please provide a valid phone number. Try again")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        form = UserForm(request.POST)

        rp = request.POST
        print rp

        # print "form", form
        if User.objects.filter(username=rp.get('username')).exists() or User.objects.filter(
                email=rp.get('email')).exists():
            messages.warning(request, "Combination of Username and email already exists. Please enter a different username and/or email")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            if form.is_valid():
                user = form.save(commit=False)
                password = rp.get('password')
                password1 = rp.get('password2')
                if password != password1:
                    messages.warning(request, "Password mismatch. Try again")
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                if len(password) < 6:
                    messages.warning(request, "Password less than six characters in length")
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                user.set_password(user.password)
                user.date_joined = timezone.now().date()
                user.save()
                # print user
                username = user.username

                user_login = authenticate(username=username, password=password)
                UserAccount.objects.create(user=user_login,
                    profile_updated=True,
                    phone_number=request.POST.get('phone_number'))
                # print user_login

                if user_login:
                    # Is the account active? It could have been disabled.
                    if user_login.is_active:
                        # If the account is valid and active, we can log the user in.
                        # We'll send the user back to the homepage.
                        login(request, user_login)
                        messages.success(request, "Sign up was successful")
                        text = 'general/Welcome_email.txt'
                        user = request.user
                        try:
                            subject = "Welcome to look-fab.com"
                            look_fab_sendmail(request, user, subject, text, None)
                        except Exception as e:
                            print 'reg email error: ',e
                            pass
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.success(request, "Sign up was not successful. Try again")
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                ''' try this '''
                # new_user_acc_obj = UserAccount.objects.create(user=user)
            else:
                print form.errors
    else:
        response = redirect(reverse('general:homepage'))
        return redirect(request.META.get('HTTP_REFERER', '/'))


def confirm_paypal_payment(request):
    # print "got here"
    print "session keys: ", request.session.values()

    if request.user.is_authenticated:

        if str(request.GET.get('st')) == "Completed":
            print "user is logged in"

            tx = request.GET.get('tx')
            st = request.GET.get('st')
            amount = request.GET.get('amt')
            # user = request.session['user']
            print "amount -- st -- tx", amount, st, tx

            order_items = OrderItem.objects.filter(user_obj=request.user.useraccount,ordered=False,deleted=False)
            new_package = Packages.objects.create(user=request.user.useraccount)
            new_package.tracking_number = randomNumber(8)
            new_package.total_amount = amount
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

            payment = Payments.objects.create(
                user=request.user,
                amount=amount,
                packageID = new_package.tracking_number,
                date_created=timezone.now())

            del request.session['country']
            del request.session['shippingCost']
            del request.session['subTotal']

            try:
                #user = User.objects.get(email=post.user.email)
                user = request.user.username
                pkg = new_package
                subject = "%s Package-%s Invoice" %("look-fab.com", pkg.tracking_number)
                look_fab_sendmail(request, user, subject, "general/package_invoice_email_template.html", pkg)
                print 'email was sent to',user
            except Exception as e:
                print "email not sent because:  %s" %(str(e))
                pass

            messages.success(request,"You have sucessfully paid for the items")
            return redirect(reverse('general:homepage'))
       
    return redirect(reverse('general:homepage'))

# end general functions here

# start admin functions 

@login_required
def admin(request):
    context = {}
    template_name = 'admin/adminDashboard.html'
    context['catForm'] = CategoryForm()
    context['itemForm'] = ItemForm()
    context['all_items'] = Item.objects.filter(deleted=False)
    return render(request, template_name, context)


@login_required
def all_orders(request):
    context = {}
    template_name = 'admin/orders.html'
    context['all_items'] = OrderItem.objects.filter(deleted=False)
    return render(request, template_name, context)


@login_required
def all_payments(request):
    context = {}
    template_name = 'admin/payments.html'
    context['all_items'] = Payments.objects.all()
    return render(request, template_name, context)


@login_required
def delete_item(request,pk):
    item = Item.objects.get(pk=pk)
    print "the item", item
    item.deleted = True
    item.save()
    messages.success(request, "Item has been deleted")
    return redirect(reverse('general:admin'))


@login_required
def getItem(request):
    context = {}
    template_name = 'admin/itemedit.html'
    item = Item.objects.get(pk=request.GET.get('item_pk'))
    context['itemForm'] = ItemForm(instance=item)
    context['item_pk'] = item.pk
    return render(request, template_name, context)


@login_required
def all_customers(request):
    context={}
    template_name="admin/all_customers.html"
    all_customers = UserAccount.objects.filter(user__is_staff=False)
    context['all_customers'] = all_customers
    return render(request, template_name, context)


@login_required
def edit_item(request):  
    item = Item.objects.get(pk=request.POST.get("item_pk"))
    print request.POST
    if request.method == "POST":
        if request.POST.get('bot_catcher') != "":
            messages.warning(request,"Invalid inputs detected")
            return redirect(reverse('general:admin'))

        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            itemform = form.save(commit=False)
            itemform.save()
            messages.warning(request,"Item successfully edited")
            return redirect(reverse('general:admin'))
        else:
            print form.errors
            messages.warning(request,"oops somthing went wrong. Try again and completely enter all fields")
            return redirect(reverse('general:admin'))
    return render(request, template_name, context)


@login_required
def add_item(request):
    template_name = 'admin/add_item.html'
    context = {}
    context['itemForm'] = ItemForm()
    context['all_items'] = Item.objects.filter(deleted=False)
    if request.method == "POST":
        if request.POST.get('bot_catcher') != "":
            messages.warning(request,"Invalid inputs detected")
            return redirect(reverse('general:admin'))

        form = ItemForm(request.POST,request.FILES)
        if form.is_valid():
            itemform = form.save(commit=False)
            itemform.courier_tracking_number = random_no(4)
            itemform.slug = slugify(itemform.name)
            itemform.created_by = request.user
            itemform.item_image_big = request.FILES.get('item_image_big')
            itemform.item_image_small = request.FILES.get('item_image_big')
            itemform.save()
            messages.warning(request,"Item successfully added")
            return redirect(reverse('general:admin'))
        else:
            print form.errors
            messages.warning(request,"oops somthing went wrong. Try again and completely enter all fields")
            return redirect(reverse('general:admin'))
    return render(request, template_name, context)


@login_required
def add_category(request):
    context = {}
    template_name = 'admin/add_category.html'
    context['catForm'] = CategoryForm()
    context['all_items'] = Category.objects.all()
    if request.method == "POST":
        if request.POST.get('bot_catcher') != "":
            messages.warning(request,"Invalid inputs detected")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        if Category.objects.filter(category_name = request.POST.get('category_name')).exists():
            messages.warning(request,"Category name already exists. Please enter another.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request,"Category successfully added")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            print form.errors
            messages.warning(request,"oops somthing went wrong. Try again and completely enter all fields")
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, template_name, context)

# end admin function here



