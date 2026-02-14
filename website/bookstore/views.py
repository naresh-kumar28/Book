from django.shortcuts import render

# Create your views here.

def home(req):
    return render(req, 'home.html')


#Static Page Section
def aboutUs(req):
    return render(req, 'static-pages/about-us.html')

def contactUs(req):
    return render(req, 'static-pages/contact-us.html')

def privacyPolicy(req):
    return render(req, 'static-pages/privacy-policy.html')

def termsCondition(req):
    return render(req, 'static-pages/terms-condition.html')

def returnRefund(req):
    return render(req, 'static-pages/return-refund.html')


#Shop Section
def productDetails(req):
    return render(req, 'shop/product-details.html')

def cart(req):
    return render(req, 'shop/cart.html')

def deliveryAddress(req):
    return render(req, 'shop/delivery_address.html')

def payment(req):
    return render(req, 'shop/payment.html')

def summary(req):
    return render(req, 'shop/summary.html')


# User Section
def address(req):
    return render(req, 'my-account/address.html')

def dashboard(req):
    return render(req, 'my-account/dashboard.html')

def profile(req):
    return render(req, 'my-account/profile.html')

def myOrder(req):
    return render(req, 'my-account/my-order.html')

def wishlist(req):
    return render(req, 'my-account/wishlist.html')

