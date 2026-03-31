from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from .models import *
from .forms import *
from django.utils import timezone
from datetime import timedelta



#Checkout Pages Work


@login_required
def wishlist(request):
    data = {}
    data['categories'] = Category.objects.all()

    wishlist_qs = Wishlist.objects.filter(user=request.user).select_related('product').order_by('-id')

    data['wishlist_items'] = wishlist_qs
    data['wishlist_products'] = wishlist_qs.values_list('product_id', flat=True)

    return render(request, 'account/wishlist.html', data)


@login_required
def addToWishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def removeFromWishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).first()

    if wishlist_item:
        wishlist_item.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))




@login_required
def cart(req):
    data = {}
    data['categories'] = Category.objects.all()
    
    order_qs = Order.objects.filter(user=req.user, ordered=False)

    if order_qs.exists():
        data['order'] = order_qs[0]
    else:
        data['order'] = None

    return render(req, 'shop/cart.html', data)


@login_required
def addToCart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    order_item, created = OrderItem.objects.get_or_create(
        user=request.user,
        ordered=False,
        item=product
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item=product).exists():
            order_item.qty += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, ordered=False)
        order.items.add(order_item)

    return redirect('cart')


@login_required
def minusToCart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    order_item = OrderItem.objects.filter(
        user=request.user,
        ordered=False,
        item=product
    ).first()

    if not order_item:
        return redirect('cart')

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item=product).exists():
            if order_item.qty > 1:
                order_item.qty -= 1
                order_item.save()
            else:
                return removeFromCart(request, slug)

    return redirect('cart')


@login_required
def removeFromCart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item=product).exists():
            order_item = OrderItem.objects.get(
                user=request.user,
                ordered=False,
                item=product
            )

            order.items.remove(order_item)
            order_item.delete()

    return redirect('cart')




@login_required
def deliveryAddress(req):
    return render(req, 'shop/delivery_address.html')

@login_required
def payment(req):
    return render(req, 'shop/payment.html')

@login_required
def summary(req):
    return render(req, 'shop/summary.html')

@login_required
def address(req):
    return render(req, 'account/address.html')

@login_required
def dashboard(req):
    return render(req, 'account/dashboard.html')


@login_required
def myOrder(req):
    return render(req, 'account/my-order.html')