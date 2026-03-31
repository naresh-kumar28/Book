from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from .models import *
from .forms import *
from django.utils import timezone
from datetime import timedelta
    

# Create your views here.

def home(req):
    last_24_hours = timezone.now() - timedelta(hours=24)
    one_week_ago = timezone.now() - timedelta(days=7)

    data = {}

    data['categories'] = Category.objects.all()
    data['authors'] = Author.objects.all().order_by('-created_at')
    data['oldbooks'] = Product.objects.filter(book_type__name__iexact="Old Books", status='published')
    data['newbooks'] = Product.objects.filter(book_type__name__iexact="Newely Relase", status='published')
    data['combo'] = Product.objects.filter(book_type__name__iexact="Value Combo Packs", status='published')
    data['recent_books'] = Product.objects.filter(created_at__gte=last_24_hours).order_by('-created_at')

    # recent viewed books logic
    recent_viewed = req.session.get('recent_viewed', [])
    filtered_recent = []

    for item in recent_viewed:
        if isinstance(item, int):
            filtered_recent.append({
                'id': item,
                'viewed_at': timezone.now().isoformat()
            })
        elif isinstance(item, dict) and 'id' in item and 'viewed_at' in item:
            viewed_at = timezone.datetime.fromisoformat(item['viewed_at'])
            if timezone.is_naive(viewed_at):
                viewed_at = timezone.make_aware(viewed_at)

            if viewed_at >= one_week_ago:
                filtered_recent.append(item)

    req.session['recent_viewed'] = filtered_recent

    recent_books_list = []
    for item in filtered_recent:
        book = Product.objects.filter(id=item['id'], status='published').first()
        if book:
            recent_books_list.append(book)

    data['recent_viewed_books'] = recent_books_list

    wishlist_products = []

    if req.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)

    data['wishlist_products'] = wishlist_products

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
    product = Product.objects.get(id=id)

    data['product'] = product
    data['categories'] = Category.objects.all()

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

    if req.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)

    data['wishlist_products'] = wishlist_products
    
    data['oldbooks'] = Product.objects.filter(book_type__name__iexact="Old Books", status='published')
    data['newbooks'] = Product.objects.filter(book_type__name__iexact="Newely Relase", status='published')
    data['combo'] = Product.objects.filter(book_type__name__iexact="Value Combo Packs", status='published')
    data['recent_books'] = Product.objects.filter(created_at__gte=last_24_hours).order_by('-created_at')

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

    if req.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)

    data['wishlist_products'] = wishlist_products

    return render(req, 'shop/filter.html', data)




# book_list
def newelyRelase(req):
    data = {}
    data['newbooks'] = Product.objects.filter(book_type__name__iexact='Newely Relase', status='published')
    data['categories'] = Category.objects.all()

    wishlist_products = []

    if req.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)

    data['wishlist_products'] = wishlist_products

    return render(req, 'book_list/newely_relase.html', data)



def oldBooks(req):
    data = {}
    data['oldbooks'] = Product.objects.filter(book_type__name__iexact='Old Books', status='published')
    data['categories'] = Category.objects.all()

    wishlist_products = []

    if req.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)

    data['wishlist_products'] = wishlist_products

    return render(req, 'book_list/old_books.html', data)


def recentlyAdded(req):
    data = {}
    last_24_hours = timezone.now() - timedelta(hours=24)
    data['recent_books'] = Product.objects.filter(created_at__gte=last_24_hours).order_by('-created_at')
    data['categories'] = Category.objects.all()

    wishlist_products = []

    if req.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)

    data['wishlist_products'] = wishlist_products

    return render(req, 'book_list/recently_added.html', data)



def comboBooks(req):
    data = {}
    data['combobooks'] = Product.objects.filter(book_type__name__iexact='Value Combo Packs', status='published')
    data['categories'] = Category.objects.all()

    wishlist_products = []

    if req.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)

    data['wishlist_products'] = wishlist_products

    return render(req, 'book_list/combo_books.html', data)



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

    if req.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=req.user).values_list('product_id', flat=True)

    data['wishlist_products'] = wishlist_products

    return render(req, 'shop/filter.html', data)
