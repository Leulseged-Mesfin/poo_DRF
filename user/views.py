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
            if not (user.role == 'Manager' or user.is_superuser):
                return Response(
                    {"error": "You are not authorized to create the User."},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data
            name = data.get('name')
            email = data.get('email', '').lower()
            password = data.get('password')
            re_password = data.get('re_password')
            role = data.get('role')

            if not all([name, email, password, re_password, role]):
                return Response(
                    {"error": "All fields are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if password != re_password:
                return Response(
                    {"error": "Passwords do not match."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if len(password) < 8:
                return Response(
                    {"error": "Password should be at least 8 characters long."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "User with this email already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            User.objects.create_stuff(email, name, password, role)
            return Response(
                {"message": f"{role} account created successfully."},
                status=status.HTTP_201_CREATED
            )
           
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"})


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
            user = request.user
            if (user.role == 'Manager' or user.is_superuser == True):  
                user = User.objects.all()
                serializer = UserSerializer(user, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "You are not authorized to retrive the User."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except:
            return Response(
                {"error": "An error occurred while retriving User Detail."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                
            )
        

class UpdateUserOwnView(APIView):
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

class UpdateUserView(APIView):
    def patch(self, request, pk):
        try:
            user = request.user
            if (user.role == 'Manager' or user.is_superuser == True):              
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
            if (user.role == 'Manager' or user.is_superuser):             
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