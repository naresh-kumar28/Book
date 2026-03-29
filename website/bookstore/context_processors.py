from .models import Order

def cart_data(request):
    cart_count = 0
    cart_total_items = 0

    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, ordered=False).first()

        if order:
            cart_count = order.items.count()  # total unique products
            cart_total_items = sum(item.qty for item in order.items.all())  # total quantity

    return {
        'cart_count': cart_count,
        'cart_total_items': cart_total_items,
    }