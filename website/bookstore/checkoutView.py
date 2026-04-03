from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from .models import *
from .forms import *
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models import Q



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
    context = {}

    addresses = Address.objects.filter(user=req.user).order_by('-id')
    selected_id = req.GET.get('selected')

    selected_address = None
    if selected_id:
        selected_address = addresses.filter(id=selected_id).first()

    if not selected_address and addresses.exists():
        selected_address = addresses.first()

    order = Order.objects.filter(user=req.user, ordered=False).first()

    context['addresses'] = addresses
    context['selected_address'] = selected_address
    context['order'] = order

    return render(req, 'shop/delivery_address.html', context)


@login_required
def address(req):
    context = {}

    edit_id = req.GET.get('edit')
    add_new = req.GET.get('add')
    edit_address = None

    if edit_id:
        edit_address = get_object_or_404(Address, id=edit_id, user=req.user)

    form = AddressForm(req.POST or None, instance=edit_address)

    if req.method == 'POST':
        if form.is_valid():
            address = form.save(commit=False)
            address.user = req.user
            address.save()

            if edit_address:
                messages.success(req, 'Address updated successfully!')
            else:
                messages.success(req, 'Address added successfully!')

            return redirect('address')
        else:
            messages.error(req, 'Please correct the errors below.')

    context['form'] = form
    context['addresses'] = Address.objects.filter(user=req.user).order_by('-id')
    context['edit_address'] = edit_address
    context['show_form'] = True if edit_address or add_new or req.method == 'POST' else False

    return render(req, 'account/address.html', context)

@login_required
def delete_address(req, id):
    address = get_object_or_404(Address, id=id, user=req.user)
    address.delete()
    messages.success(req, 'Address deleted successfully!')
    return redirect('address')



@login_required
def payment(req):
    context = {}

    order = Order.objects.filter(user=req.user, ordered=False).first()
    addresses = Address.objects.filter(user=req.user).order_by('-id')

    address_id = req.GET.get('address')
    payment_method = req.GET.get('method', 'upi')

    selected_address = None

    if address_id:
        selected_address = addresses.filter(id=address_id).first()

    if not selected_address and addresses.exists():
        selected_address = addresses.first()

    context['order'] = order
    context['addresses'] = addresses
    context['selected_address'] = selected_address
    context['payment_method'] = payment_method

    return render(req, 'shop/payment.html', context)



@login_required
def placeOrder(req):
    if req.method == "POST":
        order = Order.objects.filter(user=req.user, ordered=False).first()

        if not order or not order.items.exists():
            messages.error(req, "Your cart is empty.")
            return redirect('cart')

        address_id = req.POST.get('address_id')
        payment_method = req.POST.get('payment_method')

        address = Address.objects.filter(id=address_id, user=req.user).first()

        if not address:
            messages.error(req, "Please select a valid address.")
            return redirect('delivery_address')

        order.address = address
        order.payment_method = payment_method
        order.ordered = True
        order.ordered_date = timezone.now()
        # TOTAL PRICE SAVE KARO
        order.total_price = order.get_total()
        order.save()

        order.items.update(ordered=True)

        return redirect('order_success', order_id=order.id)

    return redirect('home')


@login_required
def summary(req):
    context = {}

    order = Order.objects.filter(user=req.user, ordered=False).first()
    addresses = Address.objects.filter(user=req.user).order_by('-id')

    address_id = req.GET.get('address')
    payment_method = req.GET.get('method', 'cod')

    selected_address = None

    if address_id:
        selected_address = addresses.filter(id=address_id).first()

    if not selected_address and addresses.exists():
        selected_address = addresses.first()

    context['order'] = order
    context['selected_address'] = selected_address
    context['payment_method'] = payment_method

    return render(req, 'shop/summary.html', context)



@login_required
def dashboard(req):
    context = {}

    addresses = Address.objects.filter(user=req.user).order_by('-id')

    user_orders = Order.objects.filter(user=req.user, ordered=True)

    total_spent = user_orders.aggregate(total=Sum('total_price'))['total'] or 0

    last_30_days = timezone.now() - timedelta(days=30)
    recent_orders = user_orders.filter(
        ordered_date__gte=last_30_days
    ).count()

    context['addresses'] = addresses
    context['total_spent'] = total_spent
    context['recent_orders'] = recent_orders

    return render(req, 'account/dashboard.html', context)





@login_required
def myOrder(req):
    context = {}

    search_query = req.GET.get('search', '').strip()
    status_filter = req.GET.get('status', '').strip()

    orders = Order.objects.filter(
        user=req.user,
        ordered=True
    ).prefetch_related('items__item').select_related('address', 'coupon').order_by('-ordered_date', '-id')

    if search_query:
        if search_query.upper().startswith('ORD-'):
            cleaned_search = search_query.upper().replace('ORD-', '').lstrip('0')
            orders = orders.filter(
                Q(id__icontains=cleaned_search) |
                Q(id__icontains=search_query)
            )
        else:
            orders = orders.filter(id__icontains=search_query)

    # simple status logic
    if status_filter == 'pending':
        orders = orders.filter(delivered=False, cancelled=False)
    elif status_filter == 'delivered':
        orders = orders.filter(delivered=True, cancelled=False)
    elif status_filter == 'cancelled':
        orders = orders.filter(cancelled=True)

    context['orders'] = orders
    context['search_query'] = search_query
    context['status_filter'] = status_filter

    return render(req, 'account/my-order.html', context)


@login_required
def cancelOrder(req, order_id):
    order = get_object_or_404(Order, id=order_id, user=req.user, ordered=True)

    if not order.delivered and not order.cancelled:
        order.cancelled = True
        order.save()
        messages.success(req, 'Order cancelled successfully!')

    return redirect('my-order')


@login_required
def orderDetails(req, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__item').select_related('address', 'coupon'),
        id=order_id,
        user=req.user,
        ordered=True
    )

    context = {
        'order': order,
    }
    return render(req, 'account/order-details.html', context)


@login_required
def orderSuccess(req, order_id):
    order = get_object_or_404(Order, id=order_id, user=req.user, ordered=True)

    estimated_delivery_start = order.ordered_date + timedelta(days=3)
    estimated_delivery_end = order.ordered_date + timedelta(days=5)

    context = {
        'order': order,
        'estimated_delivery_start': estimated_delivery_start,
        'estimated_delivery_end': estimated_delivery_end,
    }

    return render(req, 'shop/order_success.html', context)