from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    #Static pages
    path('about-us/', aboutUs, name='about-us'),
    path('contact-us/', contactUs, name='contact-us'),
    path('privacy-policy/',privacyPolicy , name='privacy-policy'),
    path('terms-condition/',termsCondition , name='terms-condition'),
    path('return-refund/',returnRefund , name='return-refund'),

    #Shop Section
    path('shop/product-details/', productDetails, name='product-details'),
    path('shop/cart/', cart, name='cart'),
    path('shop/payment/', payment, name='payment'),
    path('shop/summary/', summary, name='summary'),

    # User Section
    path('user/address/', address, name='address'),
    path('user/profile/', profile, name='profile'),
    path('user/dashboard/', dashboard, name='dashboard'),
    path('user/my-order/', myOrder, name='my-order'),
    path('user/wishlist/', wishlist, name='wishlist'),
]
