
# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)
#     total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

#     class Meta:
#         model = Order
#         fields = ['customer', 'status', 'order_date', 'total_amount', 'items']
#         # fields = ['customer', 'status', 'items']
#         extra_kwargs = {
#             # 'items': {'read_only': True}, # Make 'items' read-only
#             'total_amount': {'required': False},
#             'total_amount': {'read_only': True}, # Make 'total_amount' read-only
#         }

    

    # def create(self, validated_data):
    #     items_data = validated_data.pop('items')

    #     # First, create the Order instance without items
    #     order = Order.objects.create(**validated_data)

    #     # Process each item in the order
    #     for item_data in items_data:
    #         product = item_data['product']
    #         quantity = item_data['quantity']

    #         # Validate stock availability before creating the OrderItem
    #         if product.stock < quantity:
    #             # If stock is insufficient, delete the order and raise an error
    #             order.delete()
    #             raise serializers.ValidationError(
    #                 f"Insufficient stock for {product.name}. Available stock is {product.stock}, but {quantity} was requested."
    #             )

    #         # Deduct the quantity from the product's stock
    #         product.stock -= quantity
    #         product.save()  # Save the updated stock value

    #         # Create the OrderItem and associate it with the Order
    #         OrderItem.objects.create(order=order, product=product, quantity=quantity)

    #     return order


    # def create(self, validated_data):
    #     items_data = validated_data.pop('items')

    #     # Validate all items and deduct stock before creating the Order
    #     for item_data in items_data:
    #         product = item_data['product']
    #         quantity = item_data['quantity']

    #         # Check stock again and deduct directly here
    #         if product.stock < quantity:
    #             raise serializers.ValidationError(
    #                 f"Insufficient stock for {product.name}. Available stock is {product.stock}, but {quantity} was requested."
    #             )

    #         # Temporarily deduct stock for this item
    #         product.stock -= quantity
    #         product.save()

    #     # Create the order after stock is deducted for all items
    #     order = Order.objects.create(**validated_data)

    #     # Add each OrderItem to the newly created Order
    #     for item_data in items_data:
    #         OrderItem.objects.create(order=order, **item_data)

    #     return order


    # def create(self, validated_data):
    #     items_data = validated_data.pop('items')

    #     # Use a transaction to ensure atomicity
    #     with transaction.atomic():
    #         # Create the Order instance
    #         order = Order.objects.create(**validated_data)

    #         # Create each OrderItem
    #         for item_data in items_data:
    #             # This will call OrderItemSerializer.validate() for each item
    #             product = item_data['product']
    #             quantity = item_data['quantity']
                
    #             # Reduce product stock
    #             product.stock -= quantity
    #             product.save()

    #             # Create the OrderItem and associate with the Order
    #             OrderItem.objects.create(order=order, **item_data)

    #         return order
    
    # def create(self, validated_data):
    #     """example_relationship = validated_data.pop('example_relationship')
    #         instance = ExampleModel.objects.create(**validated_data)
    #         instance.example_relationship = example_relationship
    #         return instance"""

    #     items_data = validated_data.pop('items')
    #     order = Order.objects.create(**validated_data)

        
    #     # Create each OrderItem and associate with the order
    #     for item_data in items_data:
    #         OrderItem.objects.create(order=order, **item_data)
        
    #     # Update total_amount after creating all order items
    #     order.total_amount = order.get_total_price()
    #     order.save()
        
    #     return order

    # def update(self, instance, validated_data):
    #     # Update the `Order` instance
    #     items_data = validated_data.pop('items', None)
    #     instance.customer = validated_data.get('customer', instance.customer)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.save()

    #     if items_data is not None:
    #         # Clear existing items and replace with the new ones
    #         instance.items.all().delete()
    #         for item_data in items_data:
    #             OrderItem.objects.create(order=instance, **item_data)

    #     return instance