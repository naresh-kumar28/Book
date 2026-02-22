from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required 
    

# Create your views here.

def home(req):
    return render(req, 'home.html')


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
def productDetails(req):
    return render(req, 'shop/product-details.html')

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
    return render(req, 'admin/manage_category.html')

def manageProduct(req):
    return render(req, 'admin/manage_product.html')