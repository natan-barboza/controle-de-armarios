import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Users

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
def create_user(request):
    if request.method == "GET":
        return render(request, "users/create_user.html")

    if request.method == "POST":
        full_name = request.POST.get("full-name")
        user_enterprise_id = request.POST.get("user-enterprise-id")
        user_personal_id = request.POST.get("user-personal-id")

        if Users.objects.filter(enterprise_id=user_enterprise_id).exists() or Users.objects.filter(personal_id=user_personal_id).exists():
            logger.warning(
                f"Tentativa de criação de usuário com matrícula '{user_enterprise_id}' ou CPF '{user_personal_id}' já existente. Usuário: {request.user.username}"
            )
            context = {
                'message': "Matrícula ou CPF já existe."
            }
            return render(request, "base/error/error-400.html", context)

        try:
            Users.objects.create(
                full_name=full_name,
                enterprise_id=user_enterprise_id,
                personal_id=user_personal_id,
                status=True
            )
            logger.info(
                f"Usuário criado: {full_name} (Matrícula: {user_enterprise_id}, CPF: {user_personal_id}) por {request.user.username}"
            )
            context = {
                'message': f"Colaborador {full_name} foi criado com sucesso!"
            }
            return render(request, "base/success.html", context)

        except Exception as e:
            logger.error(
                f"Erro ao criar usuário: {full_name} - {str(e)} | Requisição feita por: {request.user.username}"
            )
            context = {
                'message': f"Ocorreu um erro ao criar o colaborador: {str(e)}"
            }
            return render(request, "base/error/error-400.html", context)

@login_required(login_url='/login/')
def list_users(request):
    users = Users.objects.all()
    context = {
        'users': users
    }
    return render(request, "users/list_users.html", context)
