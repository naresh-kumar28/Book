from django.urls import path
from .views import *
from .adminView import *
from .accountView import *
from .checkoutView import *

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
    path('shop/product-details/<int:id>/', productDetails, name='product-details'),
    path('shop/cart/', cart, name='cart'),
    path('shop/add-to-cart/<slug:slug>/', addToCart, name='add-to-cart'),
    path('shop/minus-from-cart/<slug:slug>/', minusToCart, name='minus-from-cart'),
    path('shop/remove-from-cart/<slug:slug>/', removeFromCart, name='remove-from-cart'),
    path('shop/payment/', payment, name='payment'),
    path('place-order/', placeOrder, name='place_order'),
    path('shop/order-success/<int:order_id>/', orderSuccess, name='order_success'),

    path('shop/summary/', summary, name='summary'),
    path('shop/delivery_address/', deliveryAddress, name='delivery_address'),
    path('shop/filter/', filter, name='filter'),
    path('shop/filter/<slug:slug>/', filter, name='category_filter'),
    path('shop/filter/author/<slug:author_slug>/', filter, name='author_filter'),
    path('shop/filter/publisher/<slug:publisher_slug>/', filter, name='publisher_filter'),
    path('shop/recent-viewed/', recentViewedBooks, name='recent_viewed'),

    # User Section
    path('account/address/', address, name='address'),
    path('account/address/delete/<int:id>/', delete_address, name='delete-address'),

    path('account/profile/', profile, name='profile'),
    path('account/dashboard/', dashboard, name='dashboard'),
    path('account/my-order/', myOrder, name='my-order'),
    path('account/order-details/<int:order_id>/', orderDetails, name='order_details'),


    path('account/wishlist/', wishlist, name='wishlist'),
    path('account/add-to-wishlist/<slug:slug>/', addToWishlist, name='add-to-wishlist'),
    path('account/remove-from-wishlist/<slug:slug>/', removeFromWishlist, name='remove-from-wishlist'),


    #admin section
    path('admin/', adminDashboard, name='admin.dashboard'),

    path('admin/product/', manageProduct, name='admin.product'),
    path('admin/product/add/', addProduct, name='admin.product.add'),
    path('admin/product/<int:id>/edit/', editProduct, name='admin.product.edit'),
    path('admin/product/<int:id>/delete/', deleteProduct, name='admin.product.delete'),

    path('admin/category/', manageCategory, name='admin.category'),
    path('admin/category/<int:id>/edit/', editCategory, name='admin.category.edit'),
    path('admin/category/<int:id>/delete/', deleteCategory, name='admin.category.delete'),

    path('admin/studentclass/', studentClass, name='admin.studentclass'),
    path('admin/studentclass/<int:id>/edit', editStudentClass, name='admin.studentclass.edit'),
    path('admin/studentclass/<int:id>/delete', deleteStudentClass, name='admin.studentclass.delete'),

    path('admin/subject/', manageSubject, name='admin.subject'),
    path('admin/subject/<int:id>/delete/', deleteSubject, name='admin.subject.delete'),
    path('admin/subject/<int:id>/edit/', editSubject, name='admin.subject.edit'),

    path('admin/author/', manageAuthor, name='admin.author'),
    path('admin/author/<int:id>/delete/', deleteAuthor, name='admin.author.delete'),
    path('admin/author/<int:id>/edit/', editAuthor, name='admin.author.edit'),

    path('admin/brand/', manageBrand, name='admin.brand'),
    path('admin/brand/<int:id>/delete/', deleteBrand, name='admin.brand.delete'),
    path('admin/brand/<int:id>/edit/', editBrand, name='admin.brand.edit'),

    path('admin/booktype/', manageBooktype, name='admin.booktype'),
    path('admin/booktype/<int:id>/delete/', deleteBooktype, name='admin.booktype.delete'),
    path('admin/booktype/<int:id>/edit/', editBooktype, name='admin.booktype.edit'),

    path('admin/publisher/', managePublisher, name='admin.publisher'),
    path('admin/publisher/<int:id>/delete/', deletePublisher, name='admin.publisher.delete'),
    path('admin/publisher/<int:id>/edit/', editPublisher, name='admin.publisher.edit'),

    path('admin/user/', manageUser, name='admin.user'),
    path('admin/user/<int:id>/delete/', deleteUser, name='admin.user.delete'), 
    path('admin/user/role/<int:id>/', changeUserRole, name='admin.change_role'),

    #coupon
    path('admin/coupon/', manageCoupons, name='admin.coupon'),
    path('admin/coupon/<int:id>/edit/', editCoupon, name='admin.coupon.edit'),
    path('admin/coupon/<int:id>/delete/', deleteCoupon, name='admin.coupon.delete'),
    
    path('admin/apply-coupon/', apply_coupon, name='admin.apply.coupon'),
    path('admin/remove-coupon/', remove_coupon, name='admin.remove.coupon'),

    #book_list
    path('book/newely/', newelyRelase, name='book.newely'),
    path('book/old/', oldBooks, name='book.old'),
    path('book/recently/', recentlyAdded, name='book.recently'),
    path('book/combo/', comboBooks, name='book.combo'),


]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)