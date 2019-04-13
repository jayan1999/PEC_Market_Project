from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'shops/shops.html')
def shop(request):
    return render(request,'shops/shop.html')