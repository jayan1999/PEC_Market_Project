"""pecmarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import  url
from accounts.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include ('pages.urls')),
    # path('shops/',include ('shops.urls')),    
    path('accounts/',include ('accounts.urls')),   
    path('admin/', admin.site.urls),

    url(r'^customer/dashboard/$', customer_dashboard ),
    url(r'^customer/shops/$', customer_shops ),
    url(r'^customer/shop/(?P<pk>\d+)/$', customer_shop_details ),
    url(r'^customer/checkout/$', customer_checkout ),
    url(r'^customer/get_payment_qr_code/(?P<pk>\d+)/$', get_payment_qr_code ),
    url(r'^customer/status/(?P<pk>\d+)/$', customer_order_status ),
    url(r'^shopkeeper/dashboard/$', shopkeeper_dashboard ),
    url(r'^shopkeeper/orders/(?P<pk>\d+)/$', shopkeeper_order_status ),
    url(r'^shopkeeper/items/(?P<pk>\d+)/$', shopkeeper_items ),
    url(r'^shopkeeper/items/(?P<pk>\d+)/add/$', shopkeeper_items_add ),
    url(r'^shopkeeper/items/(?P<pk>\d+)/delete_item/$', shopkeeper_items_delete ),  
    url(r'^shopkeeper/items/(?P<pk>\d+)/itemdetails/(?P<pk2>\d+)/$', shopkeeper_items_itemdetails ),
    url(r'^shopkeeper/items/(?P<pk>\d+)/itemdetails/(?P<pk2>\d+)/modifyprice/$', modifyprice ),
    url(r'^shopkeeper/items/(?P<pk>\d+)/itemdetails/(?P<pk2>\d+)/modifyavailability/$', modifyavailability ),
    url(r'^shopkeeper/offers/(?P<pk>\d+)/$', shopkeeper_offers ),
    url(r'^shopkeeper/offers/(?P<pk>\d+)/add/$', shopkeeper_offers_add ),    
    url(r'^shopkeeper/offers/(?P<pk>\d+)/delete/$', shopkeeper_offers_delete ),
    url(r'^shopkeeper/orders/(?P<pk>\d+)/orderdetails/(?P<pk2>\d+)/$', shopkeeper_order_details ),
    url(r'^shopkeeper/orders/(?P<pk>\d+)/orderdetails/(?P<pk2>\d+)/confirm/$', confirm ),
    url(r'^shopkeeper/orders/(?P<pk>\d+)/orderdetails/(?P<pk2>\d+)/reject/$', reject ),
    url(r'^shopkeeper/orders/(?P<pk>\d+)/orderdetails/(?P<pk2>\d+)/deliver/$', deliver ),

    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
