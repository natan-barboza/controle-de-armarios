from django.urls import path
from . import views

urlpatterns = [
    path('entrada/', views.employee_entry, name="employee-entry"),
    path('saida/', views.employee_exit, name="employee-exit"),
    path('list/', views.list_cabinets, name="cabinets-list")
]
