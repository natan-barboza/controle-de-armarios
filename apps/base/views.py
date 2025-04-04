from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from apps.cabinets.models import Cabinets
from apps.cabinets_manager.models import EmployeeExit

def login_view(request):
    if request.method == "GET":
        return render(request, "base/login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not request.user.is_authenticated:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return HttpResponse("Credenciais inválidas.")
        else:
            return HttpResponse("Você já está logado.")

@login_required(login_url='/login/')
def logout_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse("Usuário deslogado.")
        else:
            return HttpResponse("Você não está logado.")

def root_view(request):
    context = dashboard_data()
    solicitations = EmployeeExit.objects.all()
    if request.method == "GET":
        context = {
            'all_cabinets': context[0],
            'free_cabinets': context[1],
            'reserved_cabinets': context[2],
            'in_use_cabinets': context[3],
            'solicitations': solicitations
        }
        return render(request, "base/dashboard.html", context)
    
def dashboard_data():
    cabinets = Cabinets.objects.all()

    reserved_cabinets = cabinets.filter(reserved=True).count()
    in_use_cabinets = cabinets.filter(reserved=False, status=True).count()
    free_cabinets = cabinets.filter(reserved=False, status=False).count()
    all_cabinets = cabinets.count()

    return [
        all_cabinets, 
        free_cabinets, 
        reserved_cabinets, 
        in_use_cabinets
    ]