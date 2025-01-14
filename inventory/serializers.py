from rest_framework import serializers
from .models import Product, Supplier, Order, OrderItem, CustomerInfo,  Category, Revenue
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductGetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id', 'name', 'category_name', 'description', 'buying_price', 'selling_price', 'stock', 'supplier_name', 'image']
        constraints = [
            UniqueConstraint(fields=['name', 'category_name'], name='unique_product_category')
        ]

class ProductPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        constraints = [
            UniqueConstraint(fields=['name', 'category'], name='unique_product_category')
        ]

class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # Read-only
    # product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']
        extra_kwargs = {
            'order': {'required': False},  # Make 'order' optional in the request
            'price': {'read_only': True}, # Make 'price' read-only if calculated
        }
    
    def validate(self, data):
        """
        Check if there is sufficient stock for each item.
        """
        product = data['product']
        quantity = data['quantity']

        if product.stock < quantity:
            raise serializers.ValidationError(f"Insufficient stock for {product.name}. Available stock is {product.stock}, but {quantity} was requested.")
        return data
    

    def update(self, instance, validated_data):
        # Update order fields directly
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()

        # # Update nested items
        # items_data = validated_data.pop('items', [])
        # instance.items.all().delete()  # Clear existing items
        
        
        # OrderItem.objects.create(order=instance, **item_data)
        product = instance.product
        quantity = instance.quantity

        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        
        if product.stock >= quantity:  # Ensure there is enough stock
            product.stock -= quantity  # Reduce stock by the order quantity
            product.save()
        else:
            raise ValidationError(f"Insufficient stock for {product.name}. Available stock is {product.stock}, but {instance.quantity} was requested.")


        return instance

class OrderGetSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    customer = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = ['customer', 'status', 'order_date', 'total_amount', 'items']
        # fields = ['customer', 'status', 'items']
        extra_kwargs = {
            # 'items': {'read_only': True}, # Make 'items' read-only
            'total_amount': {'required': False},
            'total_amount': {'read_only': True}, # Make 'total_amount' read-only
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['customer', 'status', 'order_date', 'total_amount', 'items']
        # fields = ['customer', 'status', 'items']
        extra_kwargs = {
            # 'items': {'read_only': True}, # Make 'items' read-only
            'total_amount': {'required': False},
            'total_amount': {'read_only': True}, # Make 'total_amount' read-only
        }
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Create the Order instance
            order = Order.objects.create(**validated_data)

            # Create each OrderItem
            for item_data in items_data:
                # This will call OrderItemSerializer.validate() for each item
                product = item_data['product']
                quantity = item_data['quantity']

                if quantity <= 0:
                    raise ValidationError("Quantity must be greater than zero.")
                

                if product.stock >= quantity:  # Ensure there is enough stock
                    product.stock -= quantity  # Reduce stock by the order quantity
                    product.save()
                else:
                    raise ValidationError(f"Insufficient stock for {product.name}. Available stock is {product.stock}, but {instance.quantity} was requested.")

                # Create the OrderItem and associate with the Order
                OrderItem.objects.create(order=order, **item_data)

            return order
    

    def update(self, instance, validated_data):
        # Update order fields directly
        instance.customer = validated_data.get('customer', instance.customer)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Update nested items
        items_data = validated_data.pop('items', [])
        instance.items.all().delete()  # Clear existing items
        
        for item_data in items_data:
            OrderItem.objects.create(order=instance, **item_data)

        return instance
    
    def partial_update(self, instance, validated_data):
        # Extract items data if provided
        items_data = validated_data.pop('items', None)
        
        # Update the Order instance fields only if provided in the PATCH request
        instance.customer = validated_data.get('customer', instance.customer)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        
        # If items are provided, modify the OrderItems accordingly
        if items_data is not None:
            # Optionally update existing items or create new ones
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        
        # If items are not provided, do not alter the existing items
        return instance

# class RevenueSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Revenue
#         fields = '__all__'