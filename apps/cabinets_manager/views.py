import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CabinetsManager, EmployeeExit, EmployeeExitHistory, History
from datetime import datetime

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
def list_all_employee_exit(request):
    list_all = EmployeeExitHistory.objects.all()
    context = {
        'solicitations': list_all
    }
    return render(request, "cabinets_manager/list_all_employee_exit.html", context)


@login_required(login_url='/login/')
def confirm_employee_exit(request, solicitation_id):
    try:
        data = get_object_or_404(EmployeeExit, id=solicitation_id)
        datetime_now = datetime.now()

        if request.method == "GET":
            context = {
                'solicitation': data
            }
            return render(request, "cabinets_manager/confirm_employee_exit.html", context)

        if request.method == "POST":
            status = request.POST.get("authorized")

            if status == 'on':
                cabinet = CabinetsManager.objects.get(cabinet_id=data.cabinet.id)

                # Edição de registros
                data.authorized = True
                data.save()
                cabinet.cabinet_id.status = False
                cabinet.final_datetime = datetime_now
                cabinet.save()
                cabinet.cabinet_id.save()

                logger.info(f"[EDIÇÃO] Armário {cabinet.cabinet_id} atualizado por {request.user}. Status definido como disponível.")

                History.objects.create(
                    cabinet=data.cabinet,
                    user=data.user,
                    authorized=data.authorized,
                    initial_datetime=cabinet.initial_datetime,
                    final_datetime=cabinet.final_datetime
                ).save()

                logger.info(f"[CRIAÇÃO] Históricos gerados por {request.user} para o armário {cabinet.cabinet_id}.")
                
                cabinet.delete()
                data.delete()

                logger.info(f"[EXCLUSÃO] Registros de CabinetsManager e EmployeeExit removidos por {request.user}.")

                context = {
                    'message': "O armário foi desvinculado do colaborador."
                }
                return render(request, "base/success.html", context)

            else:
                context = {
                    'message': "O armário não foi desvinculado do colaborador."
                }
                return render(request, "base/error/error-400.html", context)

    except Exception as e:
        logger.exception(f"[ERRO] Falha ao processar solicitação {solicitation_id} por {request.user}: {str(e)}")
        context = {
            'message': "Ocorreu um erro ao processar a solicitação."
        }
        return render(request, "base/error/error-500.html", context)
