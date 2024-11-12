from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Product, Supplier, Order, OrderItem, Category, CustomerInfo
from .serializers import (
    ProductSerializer, 
    SupplierSerializer, 
    OrderSerializer, 
    OrderItemSerializer, 
    CategorySerializer, 
    CustomerInfoSerializer
)
import logging

logger = logging.getLogger(__name__)
from django.core.exceptions import ValidationError



class ProductListCreateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Product."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Product."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )     
            serializer = ProductSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)                
                 
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ProductRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Product."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )               
            if not Product.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to update the Product."},
            #         status=status.HTTP_403_FORBIDDEN
            #     ) 
            if not Product.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(product, validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)        
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to update the Product."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )          
            if not Product.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            product = Product.objects.get(id=pk)    
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to delete the Product."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )                
            if not Product.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            Product.objects.get(id=pk).delete()
            if not Product.objects.filter(id=pk).exists():
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"error": "Failed to delete an Product."},
                    status=status.HTTP_400_BAD_REQUEST
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SupplierListCreateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Supplier."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )
            supplier = Supplier.objects.all()
            serializer = SupplierSerializer(supplier, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)                            
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            # user = request.user
            # if (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to create the Supplier."},
            #         status=status.HTTP_403_FORBIDDEN
            #     ) 
            serializer = SupplierSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            print(validated_data)
            serializer.create(validated_data)
            return Response({"message": "Supplier created successfully."}, status=status.HTTP_201_CREATED) 
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while creating the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        
class SupplierRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Supplier."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )            
            if not Supplier.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Supplier Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            supplier = Supplier.objects.get(id=pk)
            serializer = SupplierSerializer(supplier)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to update the Supplier."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )              
            if not Supplier.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Supplier Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            supplier = Supplier.objects.get(id=pk)
            serializer = SupplierSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(supplier, validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to update the Supplier."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )  
            if not Supplier.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Supplier Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            supplier = Supplier.objects.get(id=pk)    
            serializer = SupplierSerializer(supplier, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)                    
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Supplier."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )  
            if not Supplier.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Supplier Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            Supplier.objects.get(id=pk).delete()
            if not Supplier.objects.filter(id=pk).exists():
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"error": "Failed to delete an Supplier."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                    
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerListCreateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Customers."},
            #         status=status.HTTP_403_FORBIDDEN
            #     ) 
            customer = CustomerInfo.objects.all()
            serializer = CustomerInfoSerializer(customer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to create the Customer."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )               
            serializer = CustomerInfoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while creating the Customer.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class CustomerRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Customer."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )                
            if not CustomerInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Customer Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            customer = CustomerInfo.objects.get(id=pk)
            serializer = CustomerInfoSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Customer.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to update the Customer."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )                
            if not CustomerInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Customer Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            customer = CustomerInfo.objects.get(id=pk)
            serializer = CustomerInfoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(customer, validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Customer.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def patch(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to update the Customer."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )                
            if not CustomerInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Customer Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            customer = CustomerInfo.objects.get(id=pk) 
            serializer = CustomerInfoSerializer (customer, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Customer.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to delete the Customer."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )               
            if not CustomerInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            CustomerInfo.objects.get(id=pk).delete()
            if not CustomerInfo.objects.filter(user=user).exists():
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"error": "Failed to delete an Product."},
                    status=status.HTTP_400_BAD_REQUEST
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderListCreateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrieve the Order."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )               
            order = Order.objects.all()
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Orders.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to create the Order."},
            #         status=status.HTTP_403_FORBIDDEN
            #     ) 
            serializer = OrderSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save() # calls the create method in OrderSerializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while creating the Order.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class OrderRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrieve the Order."},
            #         status=status.HTTP_403_FORBIDDEN
            #     ) 
            
            if not Order.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            order = Order.objects.get(id=pk)
            serializer = OrderSerializer(order)
            # print(order)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Order.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            # Check if the order exists
            order = Order.objects.filter(id=pk).first()
            if not order:
                return Response(
                    {"error": "Order Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Initialize the serializer with the existing instance and new data
            serializer = OrderSerializer(order, data=request.data, partial=False)

            # Validate the data
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the validated data and update the instance
            # serializer.save()
            validated_data = serializer.validated_data
            serializer.update(order, validated_data)

            # Return the updated data as a response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Order. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def patch(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to update the Order."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )                
            if not Order.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Order Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            order = Order.objects.get(id=pk)    
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.partial_update(order, validated_data)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Order.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # 
    def delete(self, request, pk):
        try:
            # Retrieve the order
            order = Order.objects.filter(id=pk).first()
            
            # Check if the order exists
            if not order:
                logger.debug(f"Order with id {pk} does not exist.")
                return Response(
                    {"error": "Order does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Delete the order, which should cascade to related items
            logger.debug(f"Deleting Order with id {pk}.")
            order.delete()

            # Confirm deletion by querying again
            if not Order.objects.filter(id=pk).exists():
                logger.debug(f"Order with id {pk} successfully deleted.")
                return Response(
                    {"message": "Order and related items were successfully deleted."},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                logger.error(f"Order with id {pk} was not deleted for some reason.")
                return Response(
                    {"error": "Failed to delete the order."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"An exception occurred while deleting the order: {str(e)}")
            return Response(
                {"error": f"An error occurred while deleting the order: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class OrderItemListCreateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        try:            
            order_item = OrderItem.objects.all()
            serializer = OrderItemSerializer(order_item, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Order_Item.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderItemRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            order_item = OrderItem.objects.filter(id=pk).first()
            if not order_item:
                return Response(
                    {"error": "OrderItem Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = OrderItemSerializer(order_item)
            # print(order)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the OrderItem.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            # Check if the order_item exists
            order_item = OrderItem.objects.filter(id=pk).first()
            if not order_item:
                return Response(
                    {"error": "OrderItem Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Initialize the serializer with the existing instance and new data
            serializer = OrderItemSerializer(order_item, data=request.data, partial=False)

            # Validate the data
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the validated data and update the instance
            # serializer.save()
            validated_data = serializer.validated_data
            serializer.update(order_item, validated_data)

            # Return the updated data as a response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the OrderItem. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def patch(self, request, pk):
        try:              
            if not OrderItem.objects.filter(id=pk).exists():
                return Response(
                    {"error": "OrderItem Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            order_item = OrderItem.objects.get(id=pk)    
            serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(order_item, validated_data)
            # serializer.save()-
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the OrderItem.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # 
    def delete(self, request, pk):  
        try:
            # Retrieve the order
            order_item = OrderItem.objects.filter(id=pk).first()
            
            # Check if the order_item exists
            if not order_item:
                logger.debug(f"OrderItem with id {pk} does not exist.")
                return Response(
                    {"error": "OrderItem does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Delete the order, which should cascade to related items
            logger.debug(f"Deleting OrderItem with id {pk}.")
            order_item.delete()

            # Confirm deletion by querying again
            if not OrderItem.objects.filter(id=pk).exists():
                logger.debug(f"OrderItem with id {pk} successfully deleted.")
                return Response(
                    {"message": "OrderItem and related items were successfully deleted."},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                logger.error(f"OrderItem with id {pk} was not deleted for some reason.")
                return Response(
                    {"error": "Failed to delete the order."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"An exception occurred while deleting the order: {str(e)}")
            return Response(
                {"error": f"An error occurred while deleting the order: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )








class CategoryListCreateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Category."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )
            category = Category.objects.all()
            serializer = CategorySerializer(category, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)              
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to create the Category."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )

            serializer = CategorySerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while creating the Category.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        
class CategoryRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to retrive the Category."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )
            if not Category.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Category Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Category.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to update the Category."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )                
            if not Category.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Category Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(category, validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Category.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def patch(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to update the Category."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )                
            if not Category.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Category Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            category = Category.objects.get(id=pk)    
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Category.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            # user = request.user
            # if not (user.role == 'Manager' or user.role == 'Salesman'):
            #     return Response(
            #         {"error": "You are not authorized to delete the Category."},
            #         status=status.HTTP_403_FORBIDDEN
            #     )                
            if not Category.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            Category.objects.get(id=pk).delete()
            if not Category.objects.filter(user=user).exists():
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"error": "Failed to delete an Product."},
                    status=status.HTTP_400_BAD_REQUEST
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )