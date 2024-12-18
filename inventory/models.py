from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError




class Category(models.Model):
    name = models.CharField(max_length=100, default='', unique=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200, blank=True, null=False)
    contact_info = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.ForeignKey(Category, on_delete=models.CASCADE)
    types = models.JSONField(default=list)

    # def __str__(self):
    #     return f"Type for Category: {self.name.name}"


class Product(models.Model):
    name = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'product_type'], name='unique_product_category')
        ]

    def __str__(self):
        return self.name


class CustomerInfo(models.Model):
    name = models.CharField(max_length=255, default="Customer", null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True, default="")
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=(('Pending', 'Pending'), ('Completed', 'Completed')))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def str(self):
        return self.customer

    def get_total_price(self):
        """Calculate the total price of the entire order."""
        return sum(item.quantity * item.product.selling_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def str(self):
        return self.product
    
    def get_price(self):
        """Calculate the total price of this item."""
        return self.product.selling_price * self.quantity


@receiver(pre_save, sender=OrderItem)
def set_order_item_price(sender, instance, **kwargs):
    """Calculate price before saving the OrderItem instance."""
    instance.price = instance.get_price()

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """Update total amount in Order when an OrderItem is added, updated, or deleted."""
    order = instance.order
    order.total_amount = order.get_total_price()
    order.save()


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    total = sum(item.quantity * item.product.selling_price for item in order.items.all())
    order.total_amount = total
    order.save()
