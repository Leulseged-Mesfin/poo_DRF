from django.contrib.auth import get_user_model
User = get_user_model()
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status


class RegisterView(APIView):
    # permission_classes = (permissions.AllowAny,)
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user

            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response({"error": "You are not authorized to create the User."},status=status.HTTP_403_FORBIDDEN)

            data = request.data

            name = data['name']
            email = data['email']
            email = email.lower()
            password = data['password']
            re_password = data['re_password']
            role = data['role']

             # Validate required fields
            if not all([name, email, password, re_password, role]):
                return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

            if password != re_password:
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

            if len(password) < 8:
                return Response({"error": "Password should be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)

            if UserAccount.objects.filter(email=email).exists():
                return Response( {"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)


            # Create the user based on the role
            if role == "Manager":
                User.objects.create_manager(email=email, name=name, password=password, role=role)
                return Response({"message": "Manager account created successfully."}, status=status.HTTP_201_CREATED)

            elif role == "Salesman":
                User.objects.create_salesman(email=email, name=name, password=password, role=role)
                return Response({"message": "Salesman account created successfully."}, status=status.HTTP_201_CREATED)

            else:
                return Response( {"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)


            # if password == re_password:
            #     if len(password) >= 8:
            #         if not User.objects.filter(email=email).exists():
            #             if serializer.is_valid():
            #             # user = serializer.save()
            #                 if role == "Manager":

            #                     User.objects.create_manager(email=email, name=name, password=password, role=role)
            #                     return Response({"message": "Manager account created successfully."}, status=status.HTTP_201_CREATED)

            #                 elif role == "Salesman":

            #                     User.objects.create_salesman(email=email, name=name, password=password, role=role)
            #                     return Response({"message": "Sales account created successfully."}, status=status.HTTP_201_CREATED)

            #                 else:
            #                     return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)
            #         else:
            #             return Response({"error": "user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

            #     else:
            #         return Response({"error": "Password should be at least 8 characters long."},status=status.HTTP_400_BAD_REQUEST)

            # else:
            #     return Response({"error": "Passwords do not match."},status=status.HTTP_400_BAD_REQUEST)

                

        except:
            return Response(
                {"error": "An error occurred while registering."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                
            )



class RetriveUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {"error": "An error occurred while retriving User Detail."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR               
            )
        

class ListUserView(APIView):
    def get(self, request, format=None):
        try:
            user = User.objects.all()
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except:
            return Response(
                {"error": "An error occurred while retriving User Detail."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                
            )
        

class UpdateUserView(APIView):
    def patch(self, request, format=None):
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(
                {"error": "An error occurred while updating User Detail."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateUserOwnView(APIView):
    def patch(self, request, pk):
        try:
            user = request.user
            if (user.role == 'Manager' or user.role == 'Salesman'):              
                if not User.objects.filter(id=pk).exists():
                    return Response(
                        {"error": "User Does not Exist."},
                        status=status.HTTP_404_NOT_FOUND
                    )

                serializer = UserSerializer(user, data=request.data, partial=True)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response(
                    {"error": "You are not authorized to update the User."},
                    status=status.HTTP_403_FORBIDDEN
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the User.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteUserView(APIView):
     def delete(self, request, pk):

        try:
            user = request.user
            if (user.role == 'Manager' or user.role == 'Salesman' or user.is_superuser):             
                if not User.objects.filter(id=pk).exists():
                    return Response(
                        {"error": "User Does not Exist."},
                        status=status.HTTP_404_NOT_FOUND
                    )
                User.objects.get(id=pk).delete()
                if not User.objects.filter(id=pk).exists():
                    return Response(
                        status=status.HTTP_204_NO_CONTENT
                    )
                else:
                    return Response(
                        {"error": "Failed to delete an User."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"error": "You are not authorized to delete the User."},
                    status=status.HTTP_403_FORBIDDEN
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while deleting the User.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        

# create a model called user and fields are email, name, password and role ,
#  role is choice and define the choice inside the user model not on its 
#  own and also create registration view and use APIView.

try:
            user = request.user
            if (user.role == 'Manager' or user.role == 'Salesman'): 
                product = Product.objects.all()
                serializer = ProductSerializer(product, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "You are not authorized to retrive the Product."},
                    status=status.HTTP_403_FORBIDDEN
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )