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
    data = {}

    
    data['categories'] = Category.objects.all()
    data['authors']= Author.objects.all().order_by('-created_at')
    data['oldbooks'] = Product.objects.filter(book_type__name__iexact="Old Books", status='published')
    data['newbooks'] = Product.objects.filter(book_type__name__iexact="Newely Relase", status='published')
    data['recent_books'] = Product.objects.filter(created_at__gte=last_24_hours).order_by('-created_at')
    
    return render(req, 'home.html',data)


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
    data['product'] = Product.objects.get(id=id)
    data['categories'] = Category.objects.all()

    return render(req, 'shop/product-details.html', data)

def cart(req):
    return render(req, 'shop/cart.html')

@login_required
def deliveryAddress(req):
    return render(req, 'shop/delivery_address.html')

@login_required
def payment(req):
    return render(req, 'shop/payment.html')

@login_required
def summary(req):
    return render(req, 'shop/summary.html')


def filter(req, slug=None):
    data = {}
    data['categories'] = Category.objects.all()
    data['title'] = "All Books"

    if req.GET.get("search"):
        search = req.GET.get("search")
        data['books'] = Product.objects.filter(title__icontains=search)
        data['title'] = search

    elif slug:
        category = get_object_or_404(Category, cat_slug=slug)
        data['books'] = Product.objects.filter(category=category)
        data['title'] = category
        data['active_category_id'] = category.id

    else:
        data['books'] = Product.objects.all()

    return render(req, 'shop/filter.html', data)




# book_list
def newelyRelase(req):
    data = {}
    data['newbooks'] = Product.objects.filter(book_type__name__iexact='Newely Relase', status='published')
    data['categories'] = Category.objects.all()

    return render(req, 'book_list/newely_relase.html', data)

def oldBooks(req):
    data = {}
    data['oldbooks'] = Product.objects.filter(book_type__name__iexact='Old Books', status='published')
    data['categories'] = Category.objects.all()

    return render(req, 'book_list/old_books.html', data)


def recentlyAdded(req):

    last_24_hours = timezone.now() - timedelta(hours=24)
    recent_books = Product.objects.filter(created_at__gte=last_24_hours).order_by('-created_at')
    

    return render(req, 'book_list/recently_added.html', {"recent_books": recent_books})
