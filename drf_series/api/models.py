import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Models

class User(AbstractUser):
    """
    Custom user model

    """
    pass


class Product(models.Model):
    """
    Product model

    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    """
    Order model

    """
    class StatusChoice(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # auto_now_add=True sets the field to now when the object is first created
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=StatusChoice.choices, 
        default=StatusChoice.PENDING
    )
    # Many-to-many relationship. Watch Django ORM for this.
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
class OrderItem(models.Model):
    """
    Order item model. Link the order to products

    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_subtotal(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.order_id}"