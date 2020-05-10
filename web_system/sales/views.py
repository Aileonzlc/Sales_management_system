from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def listorders(request):
    return HttpResponse("下面是系统中所有的订单信息。。。")
