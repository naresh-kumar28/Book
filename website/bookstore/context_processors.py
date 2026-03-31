from .models import Order, Wishlist

def cart_data(request):
    cart_count = 0
    cart_total_items = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, ordered=False).first()

        if order:
            cart_count = order.items.count()
            cart_total_items = sum(item.qty for item in order.items.all())

        # Wishlist count
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return {
        'cart_count': cart_count,
        'cart_total_items': cart_total_items,
        'wishlist_count': wishlist_count,
    }