from django.urls import path
from .views import RegisterView, RetriveUserView, ListUserView, UpdateUserView, DeleteUserView, UpdateUserOwnView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('retrive', RetriveUserView.as_view()),
    path('list', ListUserView.as_view()),
    path('update', UpdateUserOwnView.as_view()),
    path('update/<pk>', UpdateUserView.as_view()),
    path('delete/<pk>', DeleteUserView.as_view()),
]