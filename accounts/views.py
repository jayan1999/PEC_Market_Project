from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from accounts.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def register(request):
    if request.method == 'POST':
        # Get form values
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        #contact_number = request.POST['contact_number']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,': The username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,': That email id is being used')
                    return redirect('register')
                else:
                    #user= User.objects.create_user(username=username,password=password, email=email,first_name=first_name,last_name=last_name,contact_number=contact_number)
                    user= User.objects.create_user(username=username,password=password, email=email,first_name=first_name,last_name=last_name)
                    user.save()
                    Customer.objects.create(auth_user = user )
                    messages.success(request,': You are now registered and can log in')
                    return redirect('login')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
        # Check if user is Shopkeeper
            try:
                Shopkeeper.objects.get(auth_user = user)
                return HttpResponseRedirect('/shopkeeper/dashboard/')
            except Shopkeeper.DoesNotExist:
                # Check if user is customer
                try:
                    Customer.objects.get(auth_user = user)
                    return HttpResponseRedirect('/customer/dashboard/')
                except Customer.DoesNotExist:
                    pass

        messages.error(request,'Invalid Credentials')
        return redirect('login')

    else:
        return render(request, 'accounts/login.html')

@login_required
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are now logged out')
        return redirect('index')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def customer_dashboard(request):
    # customer=Customer.objects.get(auth_user_email=User.email)
    return render(request, 'accounts/customer_dashboard.html')

@login_required
def customer_shops(request):
    dictV = {}
    dictV['shops'] = Shop.objects.all().order_by('pk')
    return render(request, 'accounts/customer_shop_list.html', dictV)

@login_required
def customer_shop_details(request, pk):
    dictV = {}
    dictV['shop'] = Shop.objects.get(pk = pk)
    dictV['inventory_items'] = InventoryItem.objects.filter( shop = dictV['shop'], availability__gt = 0 ).order_by('-pk')
    dictV['offers'] = Offer.objects.filter( shop = dictV['shop']).order_by('-pk')    
    return render(request, 'accounts/customer_shop_details.html', dictV)

@csrf_exempt
@login_required
def customer_checkout(request):
    dictV = {}
    if request.method == "POST" and request.POST.get('data'):

        data = json.loads(request.POST.get('data'))
        cart_items = data['items'][1:] # ignore ist one
        # get cart items
        shop_id = data['shop_id']
        # get shop id
        transaction_id = data['txID']
        customer = request.user.customer
        # get customer from request.user
        shop = Shop.objects.get(pk = shop_id)

        items = []
        total_amount = 0.0
        for item in cart_items:
            inventory_item = InventoryItem.objects.get(pk= item)
            items.append(inventory_item)
            total_amount = total_amount + inventory_item.price
            inventory_item.availability = inventory_item.availability - 1 
            inventory_item.save()

        order = Order.objects.create(
                customer = customer,
                shop = shop,
                total_price= total_amount,
                transaction_id = transaction_id,
                status = Order.STATUS_WAITING
        )
        # Create Order Object

        unique_items = list(set(cart_items))
        for item in unique_items:
            item_count = cart_items.count(item)
            OrderItem.objects.create(
                order = order,
                item = InventoryItem.objects.get(id = item),
                quantity = item_count
                )
        # generate and show order id
        order_id = order.id
        dictV['order_id'] = order_id
        dictV['status'] = 'success'
        return JsonResponse(dictV)
    return render(request, 'accounts/customer_shop_checkout.html', dictV)


@login_required
def get_payment_qr_code(request, pk ):
    """ Return qr code URL of shop with pk=pk"""
    dictV = {}
    shop = Shop.objects.get( pk = pk )
    url = shop.paytm_qr.url
    return HttpResponse(url)

# def customer_order_status(request, pk):
#     dictV = {}
#     dictV['shop'] = Shop.objects.get(pk = pk)
#     dictV['inventory_items'] = InventoryItem.objects.filter( shop = dictV['shop'], availability__gt = 0 ).order_by('-pk')
#     return render(request, 'accounts/customer_shop_details.html', dictV)

@login_required
def customer_order_status(request,pk):
    dictV = {}
    dictV['customer'] = Customer.objects.get(pk = pk)
    dictV['orders'] = Order.objects.filter( customer = dictV['customer']).order_by('-pk')
    return render(request, 'accounts/customer_order_status.html', dictV)

@login_required
def shopkeeper_dashboard(request):
    dictV = {}
    # dictV['shopkeepers'] = Shopkeeper.objects.get(email_address=User.email)
    return render(request, 'accounts/shopkeeper_dashboard.html',dictV)

@login_required
def shopkeeper_order_status(request,pk):
    dictV = {}
    dictV['shop'] = Shop.objects.get(shopkeeper=pk)
    dictV['orders'] = Order.objects.filter( shop = dictV['shop']).order_by('-pk')
    return render(request, 'accounts/shopkeeper_order_status.html',dictV)

def shopkeeper_items(request,pk):
    dictV = {}
    dictV['shop'] = Shop.objects.get(shopkeeper=pk)
    dictV['items'] = InventoryItem.objects.filter( shop = dictV['shop']).order_by('-pk')
    return render(request, 'accounts/shopkeeper_items.html',dictV)

def shopkeeper_items_itemdetails(request,pk,pk2):
    dictV = {}
    dictV['item'] = InventoryItem.objects.get(pk=pk2)
    return render(request, 'accounts/shopkeeper_items_itemdetails.html', dictV)

def shopkeeper_offers(request,pk):
    dictV = {}
    dictV['shop'] = Shop.objects.get(shopkeeper=pk)
    dictV['offers'] = Offer.objects.filter( shop = dictV['shop']).order_by('-pk')
    return render(request, 'accounts/shopkeeper_offers.html',dictV)

def shopkeeper_offers_delete(request,pk):
    if(request.method) == 'POST':
        offer_id = request.POST['offer_id']

    req_offer = Offer.objects.get(pk=offer_id)
    req_offer.delete()
    return redirect('/shopkeeper/offers/'+pk)\

def shopkeeper_items_delete(request,pk):
    if(request.method) == 'POST':
        item_id = request.POST['item_id']

    req_item = InventoryItem.objects.get(pk=item_id)
    req_item.delete()
    return redirect('/shopkeeper/items/'+pk)

def shopkeeper_items_add(request,pk):
    if(request.method) == 'POST':
        shop_id = request.POST['shop_id']
        item_name = request.POST['item_name']
        price = request.POST['price']
        availability = request.POST['availability']

    shop=Shop.objects.get(pk=shop_id)
    item = InventoryItem(shop=shop,item_name=item_name,price=price,availability=availability)
    item.save()

    return redirect('/shopkeeper/items/'+pk)\


def shopkeeper_offers_add(request,pk):
    if(request.method) == 'POST':
        shop_id = request.POST['shop_id']
        new_offer = request.POST['new_offer']

    shop=Shop.objects.get(pk=shop_id)
    offer = Offer(shop=shop,offer=new_offer)
    offer.save()

    return redirect('/shopkeeper/offers/'+pk)\





@login_required
def shopkeeper_order_details(request,pk,pk2):
    dictV = {}
    dictV['order'] = Order.objects.get(pk=pk2)
    dictV['order_items'] = OrderItem.objects.filter( order=dictV['order'])
    return render(request, 'accounts/shopkeeper_order_details.html',dictV)

@login_required
def confirm(request,pk,pk2):
    if(request.method) == 'POST':
        order_id = request.POST['order_id']
        shopkeeper_id = request.POST['shopkeeper_id']

    STATUS_ACCEPTED = "ACCEPTED"
    req_order = Order.objects.get(pk=order_id)
    req_order.status = STATUS_ACCEPTED
    req_order.save()
    return redirect('/shopkeeper/orders/'+shopkeeper_id)

@login_required
def reject(request,pk,pk2):
    if(request.method) == 'POST':
        order_id = request.POST['order_id']
        shopkeeper_id = request.POST['shopkeeper_id']

    STATUS_REJECTED = "REJECTED"
    req_order = Order.objects.get(pk=order_id)
    req_order.status = STATUS_REJECTED
    req_order.save()
    return redirect('/shopkeeper/orders/'+shopkeeper_id)

@login_required
def deliver(request,pk,pk2):
    if(request.method) == 'POST':
        order_id = request.POST['order_id']
        shopkeeper_id = request.POST['shopkeeper_id']

    STATUS_DELIVERED = "DELIVERED"
    req_order = Order.objects.get(pk=order_id)
    req_order.status = STATUS_DELIVERED
    req_order.save()
    return redirect('/shopkeeper/orders/'+shopkeeper_id)

def modifyprice(request,pk,pk2):
    if(request.method) == 'POST':
        item_id = request.POST['item_id']
        shopkeeper_id = request.POST['shopkeeper_id']
        new_price = request.POST['new_price']

    req_item = InventoryItem.objects.get(pk=item_id)
    req_item.price = new_price
    req_item .save()
    return redirect('/shopkeeper/items/'+shopkeeper_id)


def modifyavailability(request,pk,pk2):
    if(request.method) == 'POST':
        item_id = request.POST['item_id']
        shopkeeper_id = request.POST['shopkeeper_id']
        new_availability = request.POST['new_availability']

    req_item = InventoryItem.objects.get(pk=item_id)
    req_item.availability = new_availability
    req_item .save()
    return redirect('/shopkeeper/items/'+shopkeeper_id)
