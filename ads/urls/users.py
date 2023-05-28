from django.urls import path

from ads import views_users

urlpatterns = [
    path('', views_users.UserListView.as_view()),
    path('create/', views_users.UserCreateView.as_view()),
    path('update/<int:pk>', views_users.UserUpdateView.as_view()),
    path('delete/<int:pk>', views_users.UserDeleteView.as_view()),

]