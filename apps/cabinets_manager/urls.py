from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_all_employee_exit, name="employee-exit-list"),
    path('edit/<int:solicitation_id>/', views.confirm_employee_exit, name="employee-confirm-exit")
]