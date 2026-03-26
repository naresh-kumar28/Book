from django.shortcuts import render, redirect
from .models import *
from .forms import *
from functools import wraps
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator

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
        
        if not request.user.is_superuser:
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
        return redirect(manageProduct)
    return render(req, 'admin/add_product.html', {"form" : form})

@admin_required
def deleteProduct(req, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(manageProduct)

@admin_required
def editProduct(req, id):
    product = Product.objects.get(id=id)
    form = ProductInsertForm(req.POST or None, req.FILES or None, instance=product)
    
    if req.method=='POST':
        if form.is_vaid():
            data = form.save(commit=False)
            data.slug = slugify(data.title)
            data.save()
            return redirect(manageProduct)
    return render(req, 'admin/edit_product.html', {"form" : form})


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
