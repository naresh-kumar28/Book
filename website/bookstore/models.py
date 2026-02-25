from django.db import models

# Create your models here.

class Subject(models.Model):
    subject_name = models.CharField(max_length=150)
    subject_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.subject_name


class StudentClass(models.Model):
    name = models.CharField(max_length=100) # e.g., Class 10, Class 12 Science, B.Tech
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name
        

class Category(models.Model):
    cat_name = models.CharField(max_length=100)
    cat_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.cat_name


class Author(models.Model):
    author_name = models.CharField(max_length=200)
    author_image = models.ImageField(upload_to='authors/profiles/', blank=True, null=True)
    author_slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.author_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=200) # e.g., NCERT
    brand_slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.brand_name


class BookType(models.Model):
    name = models.CharField(max_length=100) # e.g., Old Books, Bestsellers
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name


class Publisher(models.Model):
    publisher_name = models.CharField(max_length=200) # e.g., Rupa Publications, Bloomsbury India
    publisher_image = models.ImageField(upload_to='publishers/logos/', blank=True, null=True, help_text="Publisher ka logo")
    publisher_slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.publisher_name


class Product(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    book_type = models.ForeignKey(BookType, on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)
    student_class = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Class/Grade")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/main/')
    cover_image = models.ImageField(upload_to='products/covers/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # --- HIGHLIGHTS ---
    language = models.CharField(max_length=50, default='Hindi')
    pages = models.PositiveIntegerField(help_text="Total number of pages")
    isbn = models.CharField(max_length=20, unique=True, verbose_name="ISBN Number")
    binding_type = models.CharField(max_length=50, help_text="e.g., Spiral, Paperback, Hardcover")
    width = models.CharField(max_length=50, help_text="e.g., 13 MM", blank=True)
    height = models.CharField(max_length=50, help_text="e.g., 19 MM", blank=True)
    weight = models.CharField(max_length=50, help_text="e.g., 117 GRAM", blank=True)
    publish_date = models.DateField(blank=True, null=True)
    quality_check = models.CharField(max_length=50, help_text="e.g., 32", blank=True)

    # --- STATUS ---
    STATUS_CHOICES = (
        ('draft', 'Draft (Hidden)'),
        ('published', 'Published (Visible)'),
        ('out_of_stock', 'Out of Stock'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    
    @property
    def discount_percentage(self):

        if self.discount_price and self.price and self.discount_price > self.price:
            percent = ((self.discount_price - self.price) / self.discount_price) * 100
            return int(percent)
        return 0
    

    @property
    def save_amount(self):
        
        if self.discount_price and self.price and self.discount_price > self.price:
            amount = self.discount_price - self.price
            return int(amount)
        return 0