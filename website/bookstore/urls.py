from django.urls import path
from .views import *

#image work
from django.conf import settings
from django.conf.urls.static import static

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
    path('shop/delivery_address/', deliveryAddress, name='delivery_address'),


    # User Section
    path('account/address/', address, name='address'),
    path('account/profile/', profile, name='profile'),
    path('account/dashboard/', dashboard, name='dashboard'),
    path('account/my-order/', myOrder, name='my-order'),
    path('account/wishlist/', wishlist, name='wishlist'),

    #admin section
    path('admin/', adminDashboard, name='admin.dashboard'),

    path('admin/category/', manageCategory, name='admin.category'),
    path('admin/category/<int:id>/delete/', deleteCategory, name='admin.category.delete'),

    path('admin/author/', manageAuthor, name='admin.author'),
    path('admin/author/<int:id>/delete/', deleteAuthor, name='admin.author.delete'),

    path('admin/brand/', manageBrand, name='admin.brand'),
    path('admin/brand/<int:id>/delete/', deleteBrand, name='admin.brand.delete'),

    path('admin/booktype/', manageBooktype, name='admin.booktype'),
    path('admin/booktype/<int:id>/delete/', deleteBooktype, name='admin.booktype.delete'),

    path('admin/publisher/', managePublisher, name='admin.publisher'),
    path('admin/publisher/<int:id>/delete/', deletePublisher, name='admin.publisher.delete'),

    path('admin/product/', manageProduct, name='admin.product'),
    path('admin/product/add/', addProduct, name='admin.product.add'),
    path('admin/product/<int:id>/delete/', deleteProduct, name='admin.product.delete'),

    path('admin/studentclass/', studentClass, name='admin.studentclass'),
    path('admin/studentclass/<int:id>/delete', deleteStudentClass, name='admin.studentclass.delete'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)