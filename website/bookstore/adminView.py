from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from functools import wraps
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        
        if not request.user.is_staff:
            return redirect('home')

        return view_func(request, *args, **kwargs)
    
    return wrapper


#admin section
@admin_required
def adminDashboard(req):
    context = {}
    context['total_books'] = Product.objects.count()
    context['total_authors'] = Author.objects.count()
    context['total_categories'] = Category.objects.count()
    context['total_users'] = User.objects.count()

    return render(req, 'admin/admin_dashboard.html', context)


@admin_required
def manageProduct(req):
    context = {}
    products = Product.objects.all()

    #paginator
    paginator = Paginator(products, 3)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['products'] = page_obj

    return render(req, 'admin/manage_product.html', context)

@admin_required
def addProduct(req):
    form = ProductInsertForm(req.POST or None, req.FILES or None)
    if form.is_valid():
        data = form.save(commit=False)
        data.slug = slugify(data.title)
        data.save()

        # multiple gallery images save karne ka logic
        gallery_images = req.FILES.getlist('gallery_images')
        for img in gallery_images:
            ProductImage.objects.create(
                product=data,
                image=img
            )

        return redirect(manageProduct)
    return render(req, 'admin/add_product.html', {"form" : form})

@admin_required
def deleteProduct(req, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(manageProduct)

@admin_required
def editProduct(req, id):
    product = get_object_or_404(Product, id=id)
    form = ProductInsertForm(req.POST or None, req.FILES or None, instance=product)

    if req.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = slugify(data.title)
            data.save()

            # old gallery images delete
            delete_image_ids = req.POST.getlist('delete_images')
            if delete_image_ids:
                images_to_delete = ProductImage.objects.filter(id__in=delete_image_ids, product=data)
                for image_obj in images_to_delete:
                    if image_obj.image:
                        image_obj.image.delete(save=False)
                    image_obj.delete()

            # new gallery images add
            gallery_images = req.FILES.getlist('gallery_images')
            for img in gallery_images:
                ProductImage.objects.create(product=data, image=img)

            return redirect(manageProduct)

    return render(req, 'admin/edit_product.html', {
        "form": form,
        "product": product,
        "gallery_images": product.gallery_images.all(),
    })


@admin_required
def manageCategory(req):
    context = {}

    form = CategoryInsertForm(req.POST or None)
    categories = Category.objects.all()

    #pagination
    paginator = Paginator(categories, 3)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context['categories'] = page_obj
    context['form'] = form

    if form.is_valid():
        data = form.save(commit=False)
        data.cat_slug = slugify(data.cat_name)
        data.save()
        return redirect(manageCategory)
    return render(req, 'admin/manage_category.html',context)

@admin_required
def editCategory(req, id):
    category = Category.objects.get(id=id)
    form = CategoryInsertForm(req.POST or None, instance=category)
    if req.method=='POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.cat_slug = slugify(data.cat_name)
            data.save()
            return redirect(manageCategory)
    return render(req, 'admin/edit_category.html', {"form":form})

@admin_required
def deleteCategory(req, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(manageCategory)


@admin_required
def studentClass(req):
    context = {}
    form = ClassInsertForm(req.POST or None)
    classes = StudentClass.objects.all()

    #pagination
    paginator = Paginator(classes, 3)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context['form'] = form
    context['classes'] = page_obj

    if form.is_valid():
        data = form.save(commit=False)
        data.slug = slugify(data.name)
        data.save()
        return redirect(studentClass)
    
    return render(req, 'admin/student_class.html', context)

@admin_required
def deleteStudentClass(req, id):
    studentclass = StudentClass.objects.get(id=id)
    studentclass.delete()
    return redirect(studentClass)

@admin_required
def editStudentClass(req, id):
    studentclass = StudentClass.objects.get(id=id)
    form = ClassInsertForm(req.POST or None, instance=studentclass)
    if req.method=='POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = slugify(data.name)
            data.save()
            return redirect(studentClass)
    return render(req, 'admin/edit_studentclass.html', {"form": form})


@admin_required
def manageSubject(req):
    context = {}
    form = SubjectInsertForm(req.POST or None)
    subjects = Subject.objects.all()

    #Pagination
    paginator = Paginator(subjects, 3)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['form'] = form
    context['subjects'] = page_obj

    if form.is_valid():
        data = form.save(commit=False)
        data.subject_slug = slugify(data.subject_name)
        data.save()
        return redirect(manageSubject)
    return render(req, 'admin/manage_subject.html', context)

@admin_required
def deleteSubject(req, id):
    subjects = Subject.objects.get(id=id)
    subjects.delete()
    return redirect(manageSubject)

@admin_required
def editSubject(req, id):
    subject = Subject.objects.get(id=id)
    form = SubjectInsertForm(req.POST or None, instance=subject)
    if req.method=='POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.subject_slug = slugify(data.subject_name)
            data.save()
            return redirect(manageSubject)
    return render(req, 'admin/edit_subject.html',{"form":form})


@admin_required
def manageAuthor(req):
    context = {}
    form = AuthorInsertForm(req.POST or None, req.FILES or None)
    authors = Author.objects.all()

    # Pagination
    paginator = Paginator(authors, 3)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context['authors'] = page_obj
    context['form'] = form

    if form.is_valid():
        data = form.save(commit=False)
        data.author_slug = slugify(data.author_name)
        data.save()
        return redirect(manageAuthor)
    return render(req, 'admin/manage_author.html', context)


@admin_required
def deleteAuthor(req, id):
    author = Author.objects.get(id=id)
    author.delete()
    return redirect(manageAuthor)

@admin_required
def editAuthor(req, id):
    author = Author.objects.get(id=id)
    form = AuthorInsertForm(req.POST or None, req.FILES or None, instance=author)
    if req.method=='POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.author_slug = slugify(data.author_name)
            data.save()
            return redirect(manageAuthor)
    return render(req, 'admin/edit_author.html',{"form":form})


@admin_required
def manageBrand(req):
    context = {}
    form = BrandInsertForm(req.POST or None)
    brands = Brand.objects.all()

    #pagination
    paginator = Paginator(brands, 3)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['brands'] = page_obj
    context['form'] = form

    if form.is_valid():
        data = form.save(commit=False)
        data.brand_slug = slugify(data.brand_name)
        data.save()
        return redirect(manageBrand)
    return render(req, 'admin/manage_brand.html', context)


@admin_required
def deleteBrand(req, id):
    brand = Brand.objects.get(id=id)
    brand.delete()
    return redirect(manageBrand)

@admin_required
def editBrand(req, id):
    brand = Brand.objects.get(id=id)
    form = BrandInsertForm(req.POST or None, instance=brand)
    if req.method=='POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.brand_slug = slugify(data.brand_name)
            data.save()
            return redirect(manageBrand)
    return render(req, 'admin/edit_brand.html', {"form": form})


@admin_required
def manageBooktype(req):
    context = {}
    form = BooktypeInsertForm(req.POST or None)
    booktypes = BookType.objects.all()

    #pagination
    paginator = Paginator(booktypes, 3)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context['booktypes'] = page_obj
    context['form'] = form

    if form.is_valid():
        data = form.save(commit=False)
        data.slug = slugify(data.name)
        data.save()
        return redirect(manageBooktype)
    return render(req, 'admin/manage_booktype.html', context)


@admin_required
def deleteBooktype(req, id):
    booktype = BookType.objects.get(id=id)
    booktype.delete()
    return redirect(manageBooktype)


@admin_required
def editBooktype(req, id):
    booktype = BookType.objects.get(id=id)
    form = BooktypeInsertForm(req.POST or None, instance=booktype)
    if req.method=='POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = slugify(data.name)
            data.save()
            return redirect(manageBooktype)
    return render(req, 'admin/edit_booktype.html', {"form": form})



@admin_required
def managePublisher(req):
    context = {}
    form = PublisherInsertForm(req.POST or None, req.FILES or None)
    publishers = Publisher.objects.all()

    #pagination
    paginator = Paginator(publishers, 1)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['publishers'] = page_obj
    context['form'] = form

    if form.is_valid():
        data = form.save(commit=False)
        data.publisher_slug = slugify(data.publisher_name)
        data.save()
        return redirect(managePublisher)

    return render(req, 'admin/manage_publisher.html', context)

@admin_required
def deletePublisher(req, id):
    publisher = Publisher.objects.all()
    publisher.delete()
    return redirect(managePublisher)

@admin_required
def editPublisher(req, id):
    publisher = Publisher.objects.get(id=id)
    form = PublisherInsertForm(req.POST or None, req.FILES or None, instance=publisher)
    if req.method=='POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.publisher_slug = slugify(data.publisher_name)
            data.save()
            return redirect(managePublisher)
    return render(req, 'admin/edit_publisher.html', {"form": form})

@admin_required
def manageUser(req):
    context = {}
    users = User.objects.all()

    #pagination
    paginator = Paginator(users, 10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['users'] = page_obj

    return render(req, 'admin/manage_user.html', context)


@admin_required
def deleteUser(req, id):
    # 1. Pehle user ko dhoondo (agar id galat hui toh 404 error dega, crash nahi hoga)
    user_to_delete = get_object_or_404(User, id=id)

    # SAFETY LOCK 1: Admin ko delete hone se bachana
    if user_to_delete.is_superuser:
        messages.error(req, "Security Alert: Aap kisi Admin ko delete nahi kar sakte!")
        return redirect(manageUser)

    # SAFETY LOCK 2: Khud ko delete hone se bachana (Extra precaution)
    if user_to_delete == req.user:
        messages.error(req, "Bhai, aap khud ka account delete nahi kar sakte!")
        return redirect(manageUser)

    # Agar upar wale dono locks cross ho gaye, iska matlab wo normal customer/staff hai
    name = user_to_delete.first_name or user_to_delete.username # Naam nikalne ke liye
    user_to_delete.delete()
    
    # Delete hone ke baad success message bhej do
    messages.success(req, f"User '{name}' successfully delete ho gaya hai.")

    return redirect(manageUser)


@admin_required
def changeUserRole(req, id):
    if req.method == 'POST':
        # User dhoondo jiska role change karna hai
        user_to_update = get_object_or_404(User, id=id)
        new_role = req.POST.get('role')

        # SAFETY LOCK: Admin khud ka role change na kar paye
        if user_to_update == req.user:
            messages.error(req, "Bhai, aap khud ka admin access remove nahi kar sakte!")
            return redirect(manageUser) 

        # Role Logic Apply Karein
        if new_role == 'admin':
            user_to_update.is_staff = True
            user_to_update.is_superuser = True
        elif new_role == 'staff':
            user_to_update.is_staff = True
            user_to_update.is_superuser = False
        elif new_role == 'customer':
            user_to_update.is_staff = False
            user_to_update.is_superuser = False

        user_to_update.save()
        messages.success(req, f"{user_to_update.first_name} ka role successfully '{new_role}' update ho gaya hai!")

    return redirect(manageUser)


@admin_required
def manageCoupons(req):
    context = {}
    coupons = Coupon.objects.all()
    form = CouponInsertForm(req.POST or None)

    if req.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(manageCoupons)

    #pagination
    paginator = Paginator(coupons, 3)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['coupons'] = page_obj
    context['form'] = form

    return render(req, 'admin/manage_coupons.html', context)



@admin_required
def editCoupon(req, id):
    coupon = Coupon.objects.get(id=id)
    form = CouponInsertForm(req.POST or None, instance=coupon)
    if req.method=='POST':
        if form.is_valid():
            form.save()
            return redirect(manageCoupons)
    return render(req, 'admin/edit_coupons.html', {"form": form})


@admin_required
def deleteCoupon(req, id):
    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    return redirect(manageCoupons)



@admin_required
def manageOrders(req):
    context = {}
    
    # 1. BASE QUERY: Sabhi valid orders nikal lo
    base_orders = Order.objects.filter(
        Q(ordered=True) | Q(cancelled=True)
    ).order_by('-ordered_date')
    
    # 2. CARDS DATA: Ye hamesha total dashboard ki summary dikhayega (Bina filter ke)
    total_orders = base_orders.count()
    completed_orders = base_orders.filter(delivered=True).count()
    cancelled_orders = base_orders.filter(cancelled=True).count()
    pending_orders = base_orders.filter(delivered=False, cancelled=False).count()

    # 3. FILTER & SEARCH LOGIC: Table me kya dikhega uske liye alag variable
    filtered_orders = base_orders
    
    # URL se parameters lo
    search_query = req.GET.get('search', '').strip()
    status_query = req.GET.get('status', '').strip()

    # ---> A. Status Filter (Dropdown ke liye)
    if status_query == 'pending':
        filtered_orders = filtered_orders.filter(delivered=False, cancelled=False)
    elif status_query == 'delivered':
        filtered_orders = filtered_orders.filter(delivered=True)
    elif status_query == 'cancelled':
        filtered_orders = filtered_orders.filter(cancelled=True)

    # ---> B. Search Filter (Text box ke liye)
    if search_query:
        # Agar customer "#ORD-15" search kare, to usme se "15" nikal lo database ke liye
        clean_id = search_query.replace('#ORD-', '').replace('#', '').strip()
        
        # Q Object ka jadu: Agar ID match ho YA Name match ho YA Email match ho
        filtered_orders = filtered_orders.filter(
            Q(id__icontains=clean_id) | 
            Q(address__name__icontains=search_query) | 
            Q(user__username__icontains=search_query) | 
            Q(user__email__icontains=search_query) |
            Q(items__item__title__icontains=search_query)
        )

    # 4. PAGINATION: Ab base_orders ki jagah filtered_orders pe pagination chalega
    paginator = Paginator(filtered_orders, 3) 
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 5. CONTEXT BHEJO
    context['orders'] = page_obj
    context['total_orders'] = total_orders
    context['completed_orders'] = completed_orders
    context['cancelled_orders'] = cancelled_orders
    context['pending_orders'] = pending_orders

    return render(req, 'admin/manage_orders.html', context)

@admin_required
def editOrders(req, id):
    orders = Order.objects.get(id=id)
    form = OrdersForm(req.POST or None, instance=orders)
    if req.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(manageOrders)
    return render(req, 'admin/edit_orders.html', {"form" : form})

@admin_required
def deleteOrders(req, id):
    Order.objects.get(id=id).delete()
    return redirect(manageOrders)