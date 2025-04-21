from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash on Delivery'),
        ('card', 'Credit Card'),
        ('paypal', 'PayPal'),
    ]
    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='card')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity