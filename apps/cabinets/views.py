from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cabinets
from apps.users.models import Users
from apps.cabinets_manager.models import CabinetsManager, EmployeeExit
import logging

logger = logging.getLogger(__name__)

def employee_entry(request):
    if request.method == "GET":
        return render(request, "cabinets/employee_entry.html")
    
    if request.method == "POST":
        user_enterprise_id = request.POST.get("user-enterprise-id")
        user_personal_id = request.POST.get("user-personal-id")

        free_cabinet = get_next_free_cabinet()
        user = verify_credentials(user_enterprise_id, user_personal_id)

        if not free_cabinet:
            logger.warning(f"Tentativa de alocação sem armários disponíveis - matrícula: {user_enterprise_id}")
            return render(request, "base/error/error-400.html", {'message': "O armário está ocupado."})

        if not user:
            logger.warning(f"Falha de autenticação - matrícula: {user_enterprise_id}")
            return render(request, "base/error/error-400.html", {'message': "As credenciais não conferem."})

        try:
            cabinet = CabinetsManager.objects.get(owner=user)
            logger.info(f"Tentativa de duplicação - usuário {user.full_name} já possui armário {cabinet.cabinet_id}")
            return render(request, "base/error/error-400.html", {'message': f"Usuário {user.full_name} já possui o armário {cabinet.cabinet_id}."})
        
        except CabinetsManager.DoesNotExist:
            try:
                set_cabinet_to_user(free_cabinet)
                logger.info(f"Status do armário {free_cabinet.id} alterado para ocupado (edição)")
                
                CabinetsManager.objects.create(cabinet_id=free_cabinet, owner=user)
                logger.info(f"Armário {free_cabinet.id} alocado para o usuário {user.full_name} (criação)")

                return render(request, "base/success.html", {'message': f"Sua chave é {free_cabinet.cabinet}."})

            except Exception as e:
                logger.error(f"Erro ao alocar armário para {user_enterprise_id}: {str(e)}")
                return render(request, "base/error/error-400.html", {'message': f"Ocorreu um erro ao alocar o armário: {str(e)}"})

def employee_exit(request):
    if request.method == "GET":
        return render(request, "cabinets/employee_exit.html")

    if request.method == "POST":
        user_enterprise_id = request.POST.get("user-enterprise-id")
        user_personal_id = request.POST.get("user-personal-id")
        cabinet_id = request.POST.get("cabinet-id")

        try:
            cabinet = CabinetsManager.objects.get(cabinet_id=cabinet_id)
            aux = get_cabinet(cabinet_id)
            user = verify_credentials(user_enterprise_id, user_personal_id)
            is_valid = verify_user_and_cabinet_number(cabinet, user_enterprise_id, user_personal_id, cabinet_id)

            if is_valid:
                solicitation = EmployeeExit.objects.create(cabinet=aux, user=user)
                logger.info(f"Solicitação de exclusão criada (Solicitação #{solicitation.id}) para o armário {cabinet_id} por {user.full_name}.")
                return render(request, "base/success.html", {
                    'message': f"Solicitação: {solicitation.id}.\nAguarde a confirmação da recepção."
                })
            else:
                logger.warning("Dados inválidos para solicitação de exclusão.")
                return render(request, "base/error/error-400.html", {
                    'message': "Não foi possível realizar a transação, dados não conferem."
                })
        except Exception as e:
            logger.error(f"Erro ao processar saída: {e}")
            return render(request, "base/error/error-400.html", {
                'message': "Todos os armários estão livres."
            })

@login_required(login_url='/login/')
def list_cabinets(request):
    cabinets = Cabinets.objects.all().order_by('cabinet')
    logger.info(f"Usuário {request.user} visualizou a lista de armários.")
    return render(request, "cabinets/list_cabinets.html", {'context': cabinets})

# Funções auxiliares

def get_cabinet(cabinet_id):
    try:
        cabinet = Cabinets.objects.get(id=cabinet_id)
        return cabinet
    except Cabinets.DoesNotExist:
        logger.warning(f"Tentativa de buscar armário inexistente (ID {cabinet_id})")
        return None

def get_next_free_cabinet():
    cabinet = Cabinets.objects.filter(status=False, reserved=False).first()
    if cabinet:
        logger.debug(f"Próximo armário livre: {cabinet.cabinet}")
        return cabinet
    logger.debug("Nenhum armário disponível no momento.")
    return None

def set_cabinet_to_user(cabinet):
    cabinet.status = True
    cabinet.save()
    logger.debug(f"Armário {cabinet.cabinet} atualizado como ocupado.")
    return cabinet

def verify_credentials(user_enterprise_id: str, user_personal_id: str):
    user = Users.objects.filter(enterprise_id=user_enterprise_id, personal_id=user_personal_id).first()
    if user:
        logger.debug(f"Credenciais verificadas para {user.full_name}.")
        return user
    logger.debug("Falha na verificação de credenciais.")
    return None

def verify_user_and_cabinet_number(cabinet, user_enterprise_id, user_personal_id, cabinet_id):
    if str(cabinet.cabinet_id) == str(cabinet_id) and \
       cabinet.owner.enterprise_id == user_enterprise_id and \
       cabinet.owner.personal_id == user_personal_id:
        logger.debug(f"Dados validados para usuário {user_enterprise_id} e armário {cabinet_id}.")
        return True
    logger.debug("Dados não conferem para verificação de armário.")
    return False
