from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

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




class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.item.title

    def get_total_price(self):
        return self.item.price * self.qty


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    alt_contact = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10)
    type = models.CharField(
        max_length=20,
        choices=(
            ("Home", "Home"),
            ("Office", "Office"),
        )
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Order #{self.id}"
    
    def get_subtotal(self):
        total = Decimal('0.00')
        for order_item in self.items.all():
            total += order_item.get_total_price() # Using your OrderItem method
        return total

    def get_shipping(self):
        subtotal = self.get_subtotal()
        if subtotal == Decimal('0.00'):
            return Decimal('0.00') # Agar cart empty hai to no shipping
        if subtotal >= Decimal('500.00'):
            return Decimal('0.00')
        return Decimal('49.00')

    def get_discount(self):
        if self.coupon and self.coupon.active:
            # Agar discount subtotal se zyada hai, toh maximum discount subtotal ke barabar hi milega
            # (Taaki order total negative na ho jaye)
            subtotal = self.get_subtotal()
            if self.coupon.discount_amount > subtotal:
                return subtotal
            return self.coupon.discount_amount
        return Decimal('0.00')

    def get_tax(self):
        # Tax calculation logic (Subtotal - Discount) par 18% GST
        taxable_amount = self.get_subtotal() - self.get_discount()
        if taxable_amount < Decimal('0.00'):
            taxable_amount = Decimal('0.00')
        return taxable_amount * Decimal('0.18')

    def get_total(self):
        # Calculate the final total
        total = self.get_subtotal() + self.get_shipping() + self.get_tax() - self.get_discount()
        
        # Ek final check taaki total kabhi zero se kam na ho
        if total < Decimal('0.00'):
            return Decimal('0.00')
            
        return total
    
    def get_mrp_total(self):
        # Ye sabhi items ka original price (MRP) calculate karega
        total = Decimal('0.00')
        for order_item in self.items.all():
            # Check if discount_price exists and is greater than price (MRP check)
            if order_item.item.discount_price and order_item.item.discount_price > order_item.item.price:
                mrp = order_item.item.discount_price
            else:
                mrp = order_item.item.price
            total += mrp * order_item.qty
        return total

    def get_product_discount(self):
        # Ye calculate karega ki product par kitna discount mila hai (MRP Total - Subtotal)
        return self.get_mrp_total() - self.get_subtotal()