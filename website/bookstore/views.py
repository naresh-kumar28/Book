from django.shortcuts import render

# Create your views here.

def home(req):
    return render(req, 'home.html')

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

def productDetails(req):
    return render(req, 'shop/product-details.html')

def cart(req):
    return render(req, 'shop/cart.html')