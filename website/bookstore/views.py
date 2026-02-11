from django.shortcuts import render

# Create your views here.

def home(req):
    return render(req, 'home.html')

def aboutUs(req):
    return render(req, 'pages/about-us.html')

def contactUs(req):
    return render(req, 'pages/contact-us.html')

def privacyPolicy(req):
    return render(req, 'pages/privacy-policy.html')

def termsCondition(req):
    return render(req, 'pages/terms-condition.html')

def returnRefund(req):
    return render(req, 'pages/return-refund.html')