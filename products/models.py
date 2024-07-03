from django.db import models

from config import settings



# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=25)


    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    locations = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    on_top = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}."
    
    def total_price(self):
        total = sum(item.product.price * item.quantity for item in self.cartitem_set.all())
        return total

    def total_items(self):
        total = sum(item.quantity for item in self.cartitem_set.all())
        return total
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart."
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} at {self.price} each"
    

class UserOrderHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_history")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - Order {self.order.id}"