from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from .models import *
from .forms import *
from django.utils import timezone
from datetime import timedelta




@login_required
def address(req):
    return render(req, 'account/address.html')

@login_required
def dashboard(req):
    return render(req, 'account/dashboard.html')


@login_required
def myOrder(req):
    return render(req, 'account/my-order.html')

def wishlist(req):
    return render(req, 'account/wishlist.html')