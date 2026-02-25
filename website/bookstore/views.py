from django.shortcuts import render, redirect
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


# User Section
@login_required
def address(req):
    return render(req, 'account/address.html')

@login_required
def dashboard(req):
    return render(req, 'account/dashboard.html')

@login_required
def profile(req):
    return render(req, 'account/profile.html')

@login_required
def myOrder(req):
    return render(req, 'account/my-order.html')

def wishlist(req):
    return render(req, 'account/wishlist.html')


#admin section

def adminDashboard(req):
    return render(req, 'admin/admin_dashboard.html')

def manageCategory(req):
    form = CategoryInsertForm(req.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        form.save()
        return redirect(manageCategory)
    return render(req, 'admin/manage_category.html',{"form" : form, "categories" : categories})

def deleteCategory(req, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(manageCategory)


def manageAuthor(req):
    form = AuthorInsertForm(req.POST or None, req.FILES or None)
    authors = Author.objects.all()
    if form.is_valid():
        form.save()
        return redirect(manageAuthor)
    return render(req, 'admin/manage_author.html', {"form" : form, "authors" : authors})

def deleteAuthor(req, id):
    author = Author.objects.get(id=id)
    author.delete()
    return redirect(manageAuthor)


def manageBrand(req):
    form = BrandInsertForm(req.POST or None)
    brands = Brand.objects.all()
    if form.is_valid():
        form.save()
        return redirect(manageBrand)
    return render(req, 'admin/manage_brand.html', {"form" : form, "brands" : brands})

def deleteBrand(req, id):
    brand = Brand.objects.get(id=id)
    brand.delete()
    return redirect(manageBrand)


def manageBooktype(req):
    form = BooktypeInsertForm(req.POST or None)
    booktypes = BookType.objects.all()
    if form.is_valid():
        form.save()
        return redirect(manageBooktype)
    return render(req, 'admin/manage_booktype.html', {"form" : form, "booktypes" : booktypes})

def deleteBooktype(req, id):
    booktype = BookType.objects.get(id=id)
    booktype.delete()
    return render(manageBooktype)


def managePublisher(req):
    form = PublisherInsertForm(req.POST or None, req.FILES or None)
    publishers = Publisher.objects.all()
    if form.is_valid():
        form.save()
        return redirect(managePublisher)

    return render(req, 'admin/manage_publisher.html', {"form" : form, "publishers" : publishers })

def deletePublisher(req, id):
    publisher = Publisher.objects.all()
    publisher.delete()
    return redirect(managePublisher)


def manageProduct(req):
    products = Product.objects.all()

    return render(req, 'admin/manage_product.html', {"products" : products})

def addProduct(req):
    form = ProductInsertForm(req.POST or None, req.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(manageProduct)
    return render(req, 'admin/add_product.html', {"form" : form})

def deleteProduct(req, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(manageProduct)


def studentClass(req):
    form = ClassInsertForm(req.POST or None)
    classes = StudentClass.objects.all()
    if form.is_valid():
        form.save()
        return redirect(studentClass)
    
    return render(req, 'admin/student_class.html', {"form": form, "classes": classes})


def deleteStudentClass(req, id):
    studentclass = StudentClass.objects.get(id=id)
    studentclass.delete()
    return redirect(studentClass)

def manageSubject(req):
    form = SubjectInsertForm(req.POST or None)
    subjects = Subject.objects.all()
    if form.is_valid():
        form.save()
        return redirect(manageSubject)
    return render(req, 'admin/manage_subject.html',{"form": form, "subjects": subjects})


def deleteSubject(req, id):
    subjects = Subject.objects.get(id=id)
    subjects.delete()
    return redirect(manageSubject)


# book_list
def newelyRelase(req):
    data = {}
    data['newbooks'] = Product.objects.filter(book_type__name__iexact='Newely Relase', status='published')

    return render(req, 'book_list/newely_relase.html', data)

def oldBooks(req):
    data = {}
    data['oldbooks'] = Product.objects.filter(book_type__name__iexact='Old Books', status='published')

    return render(req, 'book_list/old_books.html', data)


def recentlyAdded(req):

    last_24_hours = timezone.now() - timedelta(hours=24)
    recent_books = Product.objects.filter(created_at__gte=last_24_hours).order_by('-created_at')

    return render(req, 'book_list/recently_added.html', {"recent_books": recent_books})