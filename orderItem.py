class OrderItemListCreateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
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
            if not OrderItem.objects.filter(id=pk).exists():
                return Response(
                    {"error": "OrderItem Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            order_item = OrderItem.objects.get(id=pk)
            serializer = OrderSerializer(order_item)
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
            serializer = OrderSerializer(order_item, data=request.data, partial=False)

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
            serializer = OrderSerializer(order_item, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.partial_update(order_item, validated_data)
            # serializer.save()
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
