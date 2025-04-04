from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user, name="users-create"),
    path('list/', views.list_users, name="users-list"),
]
