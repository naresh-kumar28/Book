from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # --- HIGHLIGHTS ---
    language = models.CharField(max_length=50, default='Hindi')
    pages = models.PositiveIntegerField(help_text="Total number of pages")
    isbn = models.CharField(max_length=20, unique=True, blank=True, default='NA', verbose_name="ISBN Number")
    binding_type = models.CharField(max_length=50, help_text="e.g., Spiral, Paperback, Hardcover")
    width = models.CharField(max_length=50, help_text="e.g., 13 MM", blank=True)
    height = models.CharField(max_length=50, help_text="e.g., 19 MM", blank=True)
    weight = models.CharField(max_length=50, help_text="e.g., 117 GRAM", blank=True)
    publish_date = models.DateField(blank=True, null=True)
    quality_check = models.CharField(max_length=50, help_text="e.g., 32", blank=True, default='32')

    # --- STATUS ---
    STATUS_CHOICES = (
        ('draft', 'Draft (Hidden)'),
        ('published', 'Published (Visible)'),
        ('out_of_stock', 'Out of Stock'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    
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
    
    @property
    def averageReview(self):
        reviews = self.reviews.filter(status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    @property
    def countReview(self):
        reviews = self.reviews.filter(status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    @property
    def rating_percentages(self):
        reviews = self.reviews.filter(status=True)
        total = reviews.count()
        if total == 0:
            return {'five': 0, 'four': 0, 'three': 0, 'two': 0, 'one': 0}
        
        return {
            'five': (reviews.filter(rating=5).count() / total) * 100,
            'four': (reviews.filter(rating=4).count() / total) * 100,
            'three': (reviews.filter(rating=3).count() / total) * 100,
            'two': (reviews.filter(rating=2).count() / total) * 100,
            'one': (reviews.filter(rating=1).count() / total) * 100,
        }


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.product.title} Image"



class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        name = self.user.first_name if self.user.first_name else self.user.username
        return f"{name} - {self.item.title} ({self.qty})"

    def get_total_price(self):
        return self.item.price * self.qty


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Leave blank if using percentage discount")
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Minimum order amount required")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Leave blank if using flat discount")
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Maximum discount limit")

    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def clean(self):
        # Sirf ek type ka discount allowed ho
        if self.discount_amount and self.discount_percent:
            raise ValidationError("Coupon me ya to flat discount rakhiye ya percentage discount, dono nahi.")

        if not self.discount_amount and not self.discount_percent:
            raise ValidationError("Coupon me flat ya percentage me se koi ek discount dena zaruri hai.")

        if self.discount_percent and self.discount_percent > 100:
            raise ValidationError("Discount percent 100 se zyada nahi ho sakta.")

        if self.min_order_amount < 0:
            raise ValidationError("Minimum order amount negative nahi ho sakta.")

        if self.max_discount is not None and self.max_discount < 0:
            raise ValidationError("Max discount negative nahi ho sakta.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    alt_contact = models.CharField(max_length=20, blank=True, null=True)
    landmark = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    near_by = models.CharField(max_length=200, blank=True, null=True)
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
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ordered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    is_buy_now = models.BooleanField(default=False)

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
        if not self.coupon or not self.coupon.active:
            return Decimal('0.00')

        coupon = self.coupon
        subtotal = self.get_subtotal()
        now = timezone.now()

        # Date validity check
        if coupon.valid_from and now < coupon.valid_from:
            return Decimal('0.00')

        if coupon.valid_to and now > coupon.valid_to:
            return Decimal('0.00')

        # Minimum order value check
        if subtotal < coupon.min_order_amount:
            return Decimal('0.00')

        discount = Decimal('0.00')

        # Percentage coupon
        if coupon.discount_percent:
            discount = (subtotal * coupon.discount_percent) / Decimal('100')

            # Max cap apply
            if coupon.max_discount:
                discount = min(discount, coupon.max_discount)

        # Flat coupon
        elif coupon.discount_amount:
            discount = coupon.discount_amount

        # Final safety
        return min(discount, subtotal)

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
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField()  # store in rupees for your app
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True) # Agar koi fake review kare to admin isko False karke hide kar sake
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject