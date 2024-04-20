from datetime import datetime

from django.contrib import auth, messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render


from healing.medicos.models import (
    DadosMedico,
    DatasAbertas,
    Especialidades,
    is_medico,
)

from .models import Consulta, Documento


# Create your views here.
def home(request):
    if request.method == 'GET':
        medico_filtrar = request.GET.get('medico')
        # getList para pegar mais de um quando seleciondo pelo usuario
        especialidades_filtrar = request.GET.getlist('especialidades')
        medicos = DadosMedico.objects.all()
        # filtrar pelo nome do medico
        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)
        # filtrar pela especialidade -> id__in -> fltrar dentro de um range
        if especialidades_filtrar:
            medicos = medicos.filter(
                especialidade_id__in=especialidades_filtrar
            )

        # medicos = DadosMedico.objects.all()
        especialidades = Especialidades.objects.all()

        proxima_data = (
            DatasAbertas.objects.filter(user=request.user)
            .filter(data__gt=datetime.now())
            .filter(agendado=False)
            .order_by('data')
            .first()
        )
        return render(
            request,
            'paciente/home.html',
            {
                'medicos': medicos,
                'especialidades': especialidades,
                'is_medico': is_medico(request.user),
            },
        )


def escolher_horario(request, id_dados_medicos):
    if request.method == 'GET':
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = (
            DatasAbertas.objects.filter(user=medico.user)
            .filter(data__gte=datetime.now())
            .filter(agendado=False)
        )
        return render(
            request,
            'paciente/escolher_horario.html',
            {
                'medico': medico,
                'datas_abertas': datas_abertas,
                'is_medico': is_medico(request.user),
            },
        )


def agendar_horario(request, id_data_aberta):
    if request.method == 'GET':
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user, data_aberta=data_aberta
        )

        horario_agendado.save()

        # TODO: Sugestão Tornar atomico

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(
            request, constants.SUCCESS, 'Horário agendado com sucesso.'
        )

        return redirect('/pacientes/minhas_consultas/')


def minhas_consultas(request):
    if request.method == 'GET':
        # TODO: desenvolver filtros
        minhas_consultas = Consulta.objects.filter(
            paciente=request.user
        ).filter(data_aberta__data__gte=datetime.now())
        return render(
            request,
            'paciente/minhas_consultas.html',
            {
                'minhas_consultas': minhas_consultas,
                'is_medico': is_medico(request.user),
            },
        )


def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user)
        documentos = Documento.objects.filter(consulta=consulta)
        return render(
            request,
            'paciente/consulta.html',
            {
                'consulta': consulta,
                'dado_medico': dado_medico,
                # 'is_medico': is_medico(request.user),
                'documentos': documentos,
            },
        )

# TODO: Fazer validação de segurança nos restantes pontos do código
# TODO: Fazer o botão de cancelar consulta
# TODO: Dashboard