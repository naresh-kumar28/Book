from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about-us/', aboutUs, name='about-us'),
    path('contact-us/', contactUs, name='contact-us'),
    path('privacy-policy/',privacyPolicy , name='privacy-policy'),
    path('terms-condition/',termsCondition , name='terms-condition'),
    path('return-refund/',returnRefund , name='return-refund'),

    # shop 
    path('shop/product-details/', productDetails, name='product-details'),
    path('shop/cart/', cart, name='cart'),
]
