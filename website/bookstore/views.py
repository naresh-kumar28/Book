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
    

# Create your views here.

def home(req):
    last_24_hours = timezone.now() - timedelta(hours=24)
    one_week_ago = timezone.now() - timedelta(days=7)
    last_30_days = timezone.now() - timedelta(days=30)

    data = {}
    # 🔥 TOP SELLING LOGIC 🔥
    # Un products ko filter karo jo pichle 30 din mein successful orders mein gaye hain
    # Phir unki total sold quantity calculate (annotate) karo, aur sabse zyada bikne wale ko top par rakho
    top_selling_books = Product.objects.filter(
        orderitem__order__ordered=True, # Sirf wo item jo order ho chuke hain
        orderitem__order__ordered_date__gte=last_30_days, # Pichle 1 mahine mein
        status='published'
    ).annotate(total_sold=Sum('orderitem__qty')).order_by('-total_sold')[:10] # Top 10 nikal lo homepage ke liye

    data['top_selling_books'] = top_selling_books
    data['categories'] = Category.objects.all()
    data['authors'] = Author.objects.all().order_by('-created_at')
    data['oldbooks'] = Product.objects.filter(book_type__name__iexact="Old Books", status='published')
    data['newbooks'] = Product.objects.filter(book_type__name__iexact="Newely Relase", status='published')
    data['combo'] = Product.objects.filter(book_type__name__iexact="Value Combo Packs", status='published')
    data['recent_books'] = Product.objects.filter(created_at__gte=last_24_hours, status='published').order_by('-created_at')

    recent_viewed = req.session.get('recent_viewed', [])
    filtered_recent = []

    for item in recent_viewed:
        # 🔹 Agar purana format sirf int me saved hai
        if isinstance(item, int):
            filtered_recent.append({
                'id': item,
                'viewed_at': timezone.now().isoformat()
            })

        # 🔹 Agar naya format dict hai aur viewed_at bhi hai
        elif isinstance(item, dict) and 'id' in item and 'viewed_at' in item:
            viewed_at = timezone.datetime.fromisoformat(item['viewed_at'])

            # 🔹 Agar datetime naive hai to aware banao
            if timezone.is_naive(viewed_at):
                viewed_at = timezone.make_aware(viewed_at)

            # 🔹 Sirf last 7 days wale items rakho
            if viewed_at >= one_week_ago:
                filtered_recent.append(item)

    # 🔹 Session me cleaned recent_viewed dobara save kar diya
    req.session['recent_viewed'] = filtered_recent

    # 🔹 Recent viewed ids se actual published books nikalo
    recent_books_list = []
    for item in filtered_recent:
        book = Product.objects.filter(id=item['id'], status='published').first()
        if book:
            recent_books_list.append(book)

    data['recent_viewed_books'] = recent_books_list

    # ==============================
    # Wishlist + Cart logic
    # ==============================
    wishlist_products = []
    cart_product_ids = []

    if req.user.is_authenticated:
        # 🔹 Wishlist me jo products hain unki ids nikalo
        wishlist_products = list(
            Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)
        )

        # 🔹 User ka active cart nikalo
        order = Order.objects.filter(user=req.user, ordered=False, is_buy_now=False).first()

        if order:
            # 🔹 Cart ke andar jo OrderItems hain,
            # unse related product ki ids nikalo
            cart_product_ids = list(order.items.values_list('item_id', flat=True))

    # 🔹 Template ko wishlist ids bhejo
    data['wishlist_products'] = wishlist_products

    # 🔹 Template ko cart product ids bhejo
    # Isse har product ke liye check kar sakte ho ki wo cart me hai ya nahi
    data['cart_product_ids'] = cart_product_ids

    return render(req, 'home.html', data)


#Static Page Section
def aboutUs(req):
    return render(req, 'pages/about-us.html')


def contactUs(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        number = request.POST.get('number')

        # Email ka format taiyar karein
        full_message = f"Naya message mila hai:\n\nNaam: {name}\nContact: {number}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"

        try:
            send_mail(
                f"Website Contact: {subject}", # Subject
                full_message,                  # Message
                settings.EMAIL_HOST_USER,      # From (aapka email)
                [settings.EMAIL_HOST_USER],    # To (aapko hi mile)
                fail_silently=False,
            )
            messages.success(request, "Shukriya! Aapka message humein mil gaya hai.")
        except Exception as e:
            messages.error(request, "Maafi chahte hain, email nahi bheja ja saka. Kripya baad mein koshish karein.")
        
        return redirect('contact-us') 

    return render(request, 'pages/contact-us.html')


def privacyPolicy(req):
    return render(req, 'pages/privacy-policy.html')

def termsCondition(req):
    return render(req, 'pages/terms-condition.html')

def returnRefund(req):
    return render(req, 'pages/return-refund.html')


#Shop Section

def productDetails(req, id):
    data = {}
    last_24_hours = timezone.now() - timedelta(hours=24)
    last_30_days = timezone.now() - timedelta(days=30)
    product = get_object_or_404(Product, id=id, status='published')

    data['product'] = product
    data['categories'] = Category.objects.all()
    data['product_images'] = product.gallery_images.all()

    data['same_author_books'] = Product.objects.filter(
        author=product.author,
        status='published'
    ).exclude(id=product.id)

    data['same_publisher_books'] = Product.objects.filter(
        publisher=product.publisher,
        status='published'
    ).exclude(id=product.id)

    # recent viewed with timestamp
    recent_viewed = req.session.get('recent_viewed', [])
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    filtered_recent = []

    for item in recent_viewed:
        # old int format handle karo
        if isinstance(item, int):
            filtered_recent.append({
                'id': item,
                'viewed_at': now.isoformat()
            })
        elif isinstance(item, dict) and 'id' in item and 'viewed_at' in item:
            viewed_at = timezone.datetime.fromisoformat(item['viewed_at'])
            if timezone.is_naive(viewed_at):
                viewed_at = timezone.make_aware(viewed_at)

            if viewed_at >= one_week_ago:
                filtered_recent.append(item)

    recent_viewed = [item for item in filtered_recent if item['id'] != id]

    recent_viewed.insert(0, {
        'id': id,
        'viewed_at': now.isoformat()
    })

    recent_viewed = recent_viewed[:10]
    req.session['recent_viewed'] = recent_viewed

    recent_books = []
    for item in recent_viewed:
        if item['id'] != product.id:
            book = Product.objects.filter(id=item['id'], status='published').first()
            if book:
                recent_books.append(book)

    data['recent_viewed_books'] = recent_books

    
    wishlist_products = []
    cart_product_ids = []

    if req.user.is_authenticated:
        wishlist_products = list(
            Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)
        )

        order = Order.objects.filter(user=req.user, ordered=False, is_buy_now=False).first()

        if order:
            cart_product_ids = list(order.items.values_list('item_id', flat=True))

    data['wishlist_products'] = wishlist_products
    data['cart_product_ids'] = cart_product_ids

    
    data['oldbooks'] = Product.objects.filter(book_type__name__iexact="Old Books", status='published')
    data['newbooks'] = Product.objects.filter(book_type__name__iexact="Newely Relase", status='published')
    data['combo'] = Product.objects.filter(book_type__name__iexact="Value Combo Packs", status='published')
    data['recent_books'] = Product.objects.filter(created_at__gte=last_24_hours).order_by('-created_at')
    
    data['top_selling_books'] = Product.objects.filter(
        orderitem__order__ordered=True, # Sirf wo item jo order ho chuke hain
        orderitem__order__ordered_date__gte=last_30_days, # Pichle 1 mahine mein
        status='published'
    ).annotate(total_sold=Sum('orderitem__qty')).order_by('-total_sold')[:10] # Top 10 nikal lo homepage ke liye

    reviews = ReviewRating.objects.filter(product_id=product.id, status=True).order_by('-created_at')
    data['reviews'] = reviews

    return render(req, 'shop/product-details.html', data)


def filter(req, slug=None, author_slug=None, publisher_slug=None):
    data = {}
    data['categories'] = Category.objects.all()
    data['title'] = "All Books"

    if req.GET.get("search"):
        search = req.GET.get("search").strip()

        product = Product.objects.filter(isbn=search).first()
        if product:
            return redirect('product-details', id=product.id)

        data['books'] = Product.objects.filter(title__icontains=search)
        data['title'] = search

    elif author_slug:
        author = get_object_or_404(Author, author_slug=author_slug)
        data['books'] = Product.objects.filter(author=author)
        data['title'] = author.author_name

    elif publisher_slug:
        publisher = get_object_or_404(Publisher, publisher_slug=publisher_slug)
        data['books'] = Product.objects.filter(publisher=publisher)
        data['title'] = publisher.publisher_name

    elif slug:
        category = get_object_or_404(Category, cat_slug=slug)
        data['books'] = Product.objects.filter(category=category)
        data['title'] = category
        data['active_category_id'] = category.id

    else:
        data['books'] = Product.objects.all()

    wishlist_products = []
    cart_product_ids = []

    if req.user.is_authenticated:
        wishlist_products = list(
            Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)
        )

        order = Order.objects.filter(user=req.user, ordered=False, is_buy_now=False).first()

        if order:
            cart_product_ids = list(order.items.values_list('item_id', flat=True))

    data['wishlist_products'] = wishlist_products
    data['cart_product_ids'] = cart_product_ids

    return render(req, 'shop/filter.html', data)



# book_list
def newelyRelase(req):
    data = {}
    data['categories'] = Category.objects.all()

    data['books'] = Product.objects.filter(book_type__name__iexact='Newely Relase', status='published')
    data['title'] = "Newly Released Books"

    wishlist_products = []
    cart_product_ids = []

    if req.user.is_authenticated:
        wishlist_products = list(
            Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)
        )

        order = Order.objects.filter(user=req.user, ordered=False, is_buy_now=False).first()

        if order:
            cart_product_ids = list(order.items.values_list('item_id', flat=True))

    data['wishlist_products'] = wishlist_products
    data['cart_product_ids'] = cart_product_ids

    return render(req, 'shop/filter.html', data)


def oldBooks(req):
    data = {}
    data['categories'] = Category.objects.all()

    data['books'] = Product.objects.filter(book_type__name__iexact='Old Books', status='published')
    data['title'] = "Old Books Collection"

    wishlist_products = []
    cart_product_ids = []

    if req.user.is_authenticated:
        wishlist_products = list(
            Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)
        )

        order = Order.objects.filter(user=req.user, ordered=False, is_buy_now=False).first()

        if order:
            cart_product_ids = list(order.items.values_list('item_id', flat=True))

    data['wishlist_products'] = wishlist_products
    data['cart_product_ids'] = cart_product_ids

    return render(req, 'shop/filter.html', data)


def recentlyAdded(req):
    data = {}
    last_24_hours = timezone.now() - timedelta(hours=24)
    data['categories'] = Category.objects.all()

    data['books'] = Product.objects.filter(created_at__gte=last_24_hours).order_by('-created_at')
    data['title'] = "Recently Added Books"

    wishlist_products = []
    cart_product_ids = []

    if req.user.is_authenticated:
        wishlist_products = list(
            Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)
        )

        order = Order.objects.filter(user=req.user, ordered=False, is_buy_now=False).first()

        if order:
            cart_product_ids = list(order.items.values_list('item_id', flat=True))

    data['wishlist_products'] = wishlist_products
    data['cart_product_ids'] = cart_product_ids

    return render(req, 'shop/filter.html', data)


def comboBooks(req):
    data = {}
    data['categories'] = Category.objects.all()

    data['books'] = Product.objects.filter(book_type__name__iexact='Value Combo Packs', status='published')
    data['title'] = "Value Combo Packs"
    
    wishlist_products = []
    cart_product_ids = []

    if req.user.is_authenticated:
        wishlist_products = list(
            Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)
        )

        order = Order.objects.filter(user=req.user, ordered=False, is_buy_now=False).first()

        if order:
            cart_product_ids = list(order.items.values_list('item_id', flat=True))

    data['wishlist_products'] = wishlist_products
    data['cart_product_ids'] = cart_product_ids

    return render(req, 'shop/filter.html', data)


def recentViewedBooks(req):
    data = {}
    data['categories'] = Category.objects.all()

    recent_viewed = req.session.get('recent_viewed', [])
    one_week_ago = timezone.now() - timedelta(days=7)

    books = []

    for item in recent_viewed:
        viewed_at = timezone.datetime.fromisoformat(item['viewed_at'])
        if timezone.is_naive(viewed_at):
            viewed_at = timezone.make_aware(viewed_at)

        # sirf 7 din ke andar wale
        if viewed_at >= one_week_ago:
            book = Product.objects.filter(id=item['id'], status='published').first()
            if book:
                books.append(book)

    data['books'] = books
    data['title'] = "Your Recent Viewed Books"

    
    wishlist_products = []
    cart_product_ids = []

    if req.user.is_authenticated:
        wishlist_products = list(
            Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)
        )

        order = Order.objects.filter(user=req.user, ordered=False, is_buy_now=False).first()

        if order:
            cart_product_ids = list(order.items.values_list('item_id', flat=True))

    data['wishlist_products'] = wishlist_products
    data['cart_product_ids'] = cart_product_ids

    return render(req, 'shop/filter.html', data)


def topSellingBooks(req):
    data = {}
    data['categories'] = Category.objects.all()
    
    last_30_days = timezone.now() - timedelta(days=30)
    
    # Yahan [:10] nahi lagayenge kyunki View All me sab dikhana hai
    data['books'] = Product.objects.filter(
        orderitem__order__ordered=True,
        orderitem__order__ordered_date__gte=last_30_days,
        status='published'
    ).annotate(total_sold=Sum('orderitem__qty')).order_by('-total_sold')
    
    data['title'] = "Top Selling Books (This Month)"
    
    # Wishlist aur Cart items list 
    wishlist_products = []
    cart_product_ids = []
    if req.user.is_authenticated:
        wishlist_products = list(Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True))
        order = Order.objects.filter(user=req.user, ordered=False, is_buy_now=False).first()
        if order:
            cart_product_ids = list(order.items.values_list('item_id', flat=True))
            
    data['wishlist_products'] = wishlist_products
    data['cart_product_ids'] = cart_product_ids

    return render(req, 'shop/filter.html', data)