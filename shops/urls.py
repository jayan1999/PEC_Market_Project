from django.urls import path

from . import views

urlpatterns = [
    path('', views.index , name='shops'),
    path('<int:shop_id>', views.shop , name='shop'),
]
