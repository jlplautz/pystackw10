# Aula 2

Link para acessar diretamente no Notion:

```python
https://grizzly-amaranthus-f6a.notion.site/Aula-2-73b2e213ab074e6c8bce90c073a2e605?pvs=4
```

## Abrir horários (Médico)

Cria a model DatasAbertas:

```python
class DatasAbertas(models.Model):
    data = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agendado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.data)
```

Realize as migrações e registre no admin.py

Agora crie uma URL para abrir_horario/:

```python
path('abrir_horario/', views.abrir_horario, name="abrir_horario"),
```

Crie a view abrir_horario

```python
@login_required
def abrir_horario(request):

    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')

    if request.method == "GET":
        return render(request, 'abrir_horario.html')
```

Crie o abrir_horario.html:

```python
{% extends "base.html" %}
{% load static %}

{% block 'head' %}
    <link rel="stylesheet" href="{% static 'medicos/css/abrir_horario.css' %}">
    <link rel="stylesheet" href="{% static 'usuarios/css/usuarios.css' %}">
    <link rel="stylesheet" href="{% static 'medicos/css/cadastro_medico.css' %}">
{% endblock 'head' %}

{% block 'body' %}

    <div class="container">

        <br><br>

        <div class="row">
            <div class="col-md-8">

                <img src=""  class="foto-perfil" alt="">
                <label style="margin-left: 30px; font-size: 25px" class="p-bold">Olá, <span class="color-dark">{{request.user.username}}</span></label>
                
                <br>
                {% if messages %}
                    <br>
                    {% for message in messages %}
                        <section class="alert {{message.tags}}">
                            {{message}}
                        </section>
                    {% endfor %}
                {% endif %}
                <br>
                <p style="font-size: 25px" class="p-bold">Abrir horários para consultas</p>
                <hr>
                <form action="#" method="POST">
                    <label for="">Escolher data:</label>
                    <input type="datetime-local" name="data" class="form-control shadow-main-color">
                    <br>
                    <input type="submit" value="Salvar" class="btn btn-success btn-dark-color">
                </form>
            </div>
            <div class="col-md-4">
                <p style="font-size: 25px" class="p-bold">Seus horários:</p>
                <ul class="list-group">
                    <li>X</li>
                </ul>
            </div>
        </div>
    </div>

{% endblock 'body' %}
```

Para exibir a foto do médicos vamos precisar buscar na tabela DadosMedicos:

```python
dados_medicos = DadosMedico.objects.get(user=request.user)
return render(request, 'abrir_horario.html', {'dados_medicos': dados_medicos})
```

Agora exiba a foto do médico:

```python
{{dados_medicos.foto.url}}
```

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

Crie o abrir_horario.css:

```css
.foto-perfil{

    width: 150px;
    height: 150px;

    border-radius: 75px;

}
```

Altere o form para enviar os dados para a view:

```html
<form action="{% url 'abrir_horario' %}" method="POST">{% csrf_token %}
```

Na view processe os dados para salvar a Data:

```python
@login_required
def abrir_horario(request):

    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')

    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        return render(request, 'abrir_horario.html', {'dados_medicos': dados_medicos})
    elif request.method == "POST":
        data = request.POST.get('data')

        data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M")
        
        if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A data deve ser maior ou igual a data atual.')
            return redirect('/medicos/abrir_horario')

        horario_abrir = DatasAbertas(
            data=data,
            user=request.user
        )

        horario_abrir.save()

        messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso.')
        return redirect('/medicos/abrir_horario')
```

Para listar as datas em aberto primeiro busque no BD:

```python
datas_abertas = DatasAbertas.objects.filter(user=request.user)
return render(request, 'abrir_horario.html', {'dados_medicos': dados_medicos, 'datas_abertas': datas_abertas}
```

No HTML itere sobre os horários e os exiba:

```html
{% for data in datas_abertas  %}
    <li class="list-group-item">{{data}}</li>
{% endfor %}
```

Altere o USE_TZ para False!

## Buscar por médicos (Paciente)

Crie um APP para os paciêntes:

```html
python3 manage.py startapp paciente
```

# Instale o APP!

Crie uma URL para o APP pacientes:

```python
path('pacientes/', include('paciente.urls')),
```

Em o [urls.py](http://urls.py) no app pacientes:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
]
```

Crie a view home

```python
def home(request):
    if request.method == "GET":
        return render(request, 'home.html')
```

Crie o home.html:

```python
{% extends "base.html" %}
{% load static %}

{% block 'head' %}
    <link rel="stylesheet" href="{% static 'medicos/css/abrir_horario.css' %}">
    <link rel="stylesheet" href="{% static 'usuarios/css/usuarios.css' %}">
    <link rel="stylesheet" href="{% static 'medicos/css/cadastro_medico.css' %}">
    <link rel="stylesheet" href="{% static 'pacientes/css/home.css' %}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
{% endblock 'head' %}

{% block 'body' %}

<br><br>

<div class="container">
    <div class="row">
        <div class="col-md-8">

            <p style="font-size: 25px" class="p-bold">Olá, <span class="color-dark">{{request.user.username}}.</span></p>
            <form action="" post="GET">
                <input type="text" class="form-control shadow-main-color" placeholder="Busque por profissionais ..." name="medico">
                <br>

                <div class="especialidades">
                    <input type="checkbox" name="especialidades" value="">
                    <span class="badge bg-secondary">

                        Especialidade X
                    
                    </span>
                    

                </div>
                <br>
                <input type="submit" value="filtrar" class="btn btn-success btn-dark-color">
            </form>
            <hr>

            <div class="list-medicos">
               
                <div class="card-medicos shadow-main-color">
                    <div class="row">
                        <div class="col-md-3"><img src="#" class="foto-perfil-card" alt=""></div>
                        <div class="col-md">
                            <p style="font-size: 20px" class="p-bold">Dr(a). Nome aqui <i class="bi bi-patch-check-fill icon-main"></i></p>
                            <p>Descrição aqui</p>
                        </div>
                    </div>  
                    <p><i class="bi bi-map icon-main"></i>&nbsp&nbspRua tal aqui, 000.</p>
                    <p><i class="bi bi-calendar2-week icon-main"></i>&nbsp&nbspProxima data: 
                        00/00/0000
                        
                    <a href="#" class="btn btn-success btn-dark-color">Agendar</a>
                </div>
                <br>
                

            </div>

        </div>
        <div class="col-md-4">
            <p style="font-size: 25px" class="p-bold">Lembretes</p>

            <p class="bg-main-lembrete">
                <span class="p-bold"><i class="bi bi-exclamation-triangle-fill icon-differential"></i>&nbsp&nbsp Consulta com Pedro Sampario em 7 dias.</span>
            </p>

            
        </div>
    </div>
</div>

{% endblock 'body' %}
```

Crie o templates/static/pacientes/css/home.css:

```css
.especialidades{
    font-size: 20px;
}

.card-medicos{

    width: 60%;
    background-color: #EAEAEA;
    border: 1px solid var(--main-color);
    padding: 20px;

}

.foto-perfil-card{
    width: 90px;
    height: 90px;
    border-radius: 45px;

}

.foto-perfil-card-lg{
    width: 180px;
    height: 180px;
    border-radius: 90px;

}
.icon-main{
    color: var(--main-color);
}

.bg-main-lembrete{

    background-color: var(--dark-color);
    padding: 10px;
    color: white;
}

.icon-differential{
    color: var(--contrast-color);
}

table {
    border-collapse: collapse !important;
    width: 100%;
}

th, td {

    padding: 8px;
    text-align: center;
    background-color: #EAEAEA !important;
}

th {
    background-color: #EAEAEA;
}

.link{
    text-decoration: none;
}

.today {
    background-color: var(--dark-color);
}

.selecionar-dia{
    width: 100%;
    background-color: #EAEAEA;
    box-shadow: 1px 1px 10px gray;
}

.header-dias{
    background-color: var(--dark-color);
    padding: 15px;
    color: white;
    text-decoration: none;
}

.dia-semana{
    float: right;
}

.conteudo-data{
    padding: 15px;
    color: black;
}

.link:hover{
    text-decoration: none;
} 

.list-minhas-consultas{

    background-color: #EAEAEA;

    padding: 10px;

}

.documentos{
    background-color: #cfcfcf;
    color: black;
    padding: 20px;
    border-radius: 10px;
    font-size: 20px;
}
```

Busque todos os médicos para listagem:

```python
medicos = DadosMedico.objects.all()
```

No HTML liste todos os médicos disponíveis:

```python
{% for medico in medicos %}
  <div class="card-medicos shadow-main-color">
      <div class="row">
          <div class="col-md-3"><img src="{{medico.foto.url}}" class="foto-perfil-card" alt=""></div>
          <div class="col-md">
              <p style="font-size: 20px" class="p-bold">Dr(a). {{medico.nome}} <i class="bi bi-patch-check-fill icon-main"></i></p>
              <p>{{medico.descricao}}</p>
          </div>
      </div>  
      <p><i class="bi bi-map icon-main"></i>&nbsp&nbsp{{medico.rua}}, {{medico.numero}}.</p>
      <p><i class="bi bi-calendar2-week icon-main"></i>&nbsp&nbspProxima data: 
          
          </p>
          
      <a href="#" class="btn btn-success btn-dark-color">Agendar</a>
  </div>
  <br>
{% endfor %}
                

```

Crie o método proxima_data:

```python
proxima_data = DatasAbertas.objects.filter(user=self.user).filter(data__gt=datetime.now()).filter(agendado=False).order_by('data').first()
```

Exiba a próxima data:

```html
{% if medico.proxima_data %}
    {{medico.proxima_data}}
{% else %}
    Aguarde uma data.
{% endif %}
```

### Crie algumas especialidades!

Busque todas as especialidades:

```python
especialidades = Especialidades.objects.all()
```

Liste todas as especialidades:

```html
{% for especialidade in especialidades %}
    <input type="checkbox" name="especialidades" value="{{especialidade.id}}">
    <span class="badge bg-secondary">

        {{especialidade}}
    
    </span>
{% endfor %}
```

Envie os dados do form para a home:

```html
<form action="{% url 'home' %}" post="GET">
```

Crie os filtros:

```python
medico_filtrar = request.GET.get('medico')
especialidades_filtrar = request.GET.getlist('especialidades')

if medico_filtrar:
    medicos = medicos.filter(nome__icontains = medico_filtrar)

if especialidades_filtrar:
    medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)
```

## Escolher horário (Paciente)

Crie uma URL dinâmica para esolher_horario

```python
path('escolher_horario/<int:id_dados_medicos>/', views.escolher_horario, name="escolher_horario"),
```

Crie a view escolher_horario:

```python
def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
        return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas})
```

Crie o HTML:

```python
{% extends "base.html" %}
{% load static %}

{% block 'head' %}

    <link rel="stylesheet" href="{% static 'medicos/css/abrir_horario.css' %}">
    <link rel="stylesheet" href="{% static 'usuarios/css/usuarios.css' %}">
    <link rel="stylesheet" href="{% static 'medicos/css/cadastro_medico.css' %}">
    <link rel="stylesheet" href="{% static 'pacientes/css/home.css' %}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

{% endblock 'head' %}

{% block 'body' %}

    <div class="container">
        <br><br>

        <div class="row">
            <div class="col-md-8">

                <div class="row">
                    <div class="col-md-3"><img src="" class="foto-perfil-card" alt=""></div>
                    <div class="col-md">
                        <p style="font-size: 20px" class="p-bold">Dr(a).  <i class="bi bi-patch-check-fill icon-main"></i></p>
                        <p>desc</p>
                    </div>
                </div> 
                <br>
                {% if messages %}
                    <br>
                    {% for message in messages %}
                        <section class="alert {{message.tags}}">
                            {{message}}
                        </section>
                    {% endfor %}
                {% endif %}
                
                <hr>
                    
            
                <div class="row">
                    
                    
                        <div class="col-md-3">
                            <a class="link" href="">
                            <div class='selecionar-dia'>
                            <div class="header-dias">
                                <span class="mes">
                                mes
                                </span>
                                
                                <span class="dia-semana">
                                semana
                                </span>
                            </div>
            
                            <div class="conteudo-data">
                                data
                            </div>
                            </div>
                        </a>
                        <br>
                        </div>
                   
                    
                </div>

            </div>
            <div class="col-md-4">

            </div>
        </div>

    </div>
{% endblock 'body' %}
```

No card de cada médico em HOME redirecione para sua agenda:

```python
<a href="{% url 'escolher_horario' medico.id %}" class="btn btn-success btn-dark-color">Agendar</a>
```

Liste todos os horários em aberto:

```python
{% for data_aberta in datas_abertas %}
  <div class="col-md-3">
    <a class="link" href="#">
      <div class='selecionar-dia'>
        <div class="header-dias">
          <span class="mes">
            {{data_aberta.data.month}}
          </span>
          
          <span class="dia-semana">
            {{data_aberta.data.weekday}}
          </span>
        </div>

        <div class="conteudo-data">
          {{data_aberta.data}}
        </div>
      </div>
    </a>
    <br>
  </div>
{% endfor %}
```

## Efetivar agendamento da consulta (Paciente)

Crie a model Consulta:

```python
class Consulta(models.Model):
    status_choices = (
        ('A', 'Agendada'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
        ('I', 'Iniciada')

    )
    paciente = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data_aberta = models.ForeignKey(DatasAbertas, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices, default='A')
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.paciente.username
```

Execute as migrações e adicione ao admin.py!

Agora crie a URL agendar_horario  para efetivar o agendamento de consultas:

```python
path('agendar_horario/<int:id_data_aberta>/', views.agendar_horario, name="agendar_horario"),
```

Crie a view agendar_horario:

```python
def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )

        horario_agendado.save()

        # TODO: Sugestão Tornar atomico

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        return redirect('/pacientes/minhas_consultas/')
```

Quando o paciente clicar no card da data disponível realize o agendamento da consulta:

```python
<a class="link" href="{% url 'agendar_horario' data_aberta.id %}">
```

## Minhas consultas (Paciente)

Crie uma URL para listar todas as consultas de uma paciente:

```python
 path('minhas_consultas/', views.minhas_consultas, name="minhas_consultas"),
```

Crie a view para listar as consultas:

```python
def minhas_consultas(request):
    if request.method == "GET":
        #TODO: desenvolver filtros
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        return render(request, 'minhas_consultas.html', {'minhas_consultas': minhas_consultas})

```

Crie o HTML:

```python
{% extends "base.html" %}
{% load static %}

{% block 'head' %}

    <link rel="stylesheet" href="{% static 'medicos/css/abrir_horario.css' %}">
    <link rel="stylesheet" href="{% static 'usuarios/css/usuarios.css' %}">
    <link rel="stylesheet" href="{% static 'medicos/css/cadastro_medico.css' %}">
    <link rel="stylesheet" href="{% static 'pacientes/css/home.css' %}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

{% endblock 'head' %}

{% block 'body' %}

    <div class="container">
        <br>
        <h2><span class="color-dark">Suas consultas</span></h2>

        <div class="row">

            <div class="col-md">
                <input type="text" name="especialidades" id="" class="form-control shadow-main-color" placeholder="Especialidades médias">
            </div>
            <div class="col-md">
                <input type="date" name="data" id="" class="form-control shadow-main-color" placeholder="Data da consulta">

            </div>
            <div class="col-md">
                <input type="submit" value="Filtrar" class="btn btn-dark-color-outline">
            </div>
        </div>

        <br>

        <div class="list-minhas-consultas">
            <table class="table">
                <thead>
                  <tr>
                    <th scope="col">Médico</th>
                    <th scope="col">Status</th>
                    <th scope="col">Data</th>
                  </tr>
                </thead>
                <tbody>
                    {% for consulta in minhas_consultas  %}
                        <tr>
                            <td><a href="#">Dr(a). Nome</a></td>
                            <td>Status</td>
                            <td>Data</td>
                        </tr>
                    {% endfor %}
                </tbody>
              </table>

        </div>

    </div>

{% endblock 'body' %}
```

Exiba os dados da consulta:

```python
{% for consulta in minhas_consultas  %}
    <tr>
        <td><a href="#">Dr(a). {{consulta.data_aberta.user}}</a></td>
        <td>{{consulta.get_status_display}}</td>
        <td>{{consulta.data_aberta.data}}</td>
    </tr>
{% endfor %}
```

## Minhas consultas (Médico)

Crie uma URL para listar as consultas do médico:

```python
path('consultas_medico/', views.consultas_medico, name="consultas_medico"),
```

Crie a view:

```python
def consultas_medico(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    
    hoje = datetime.now().date()

    consultas_hoje = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje + timedelta(days=1))
    consultas_restantes = Consulta.objects.exclude(id__in=consultas_hoje.values('id'))

    return render(request, 'consultas_medico.html', {'consultas_hoje': consultas_hoje, 'consultas_restantes': consultas_restantes, 'is_medico': is_medico(request.user)})

```

Desenvolva o HTML:

```html
{% extends "base.html" %}
{% load static %}

{% block 'head' %}

    <link rel="stylesheet" href="{% static 'medicos/css/abrir_horario.css' %}">
    <link rel="stylesheet" href="{% static 'usuarios/css/usuarios.css' %}">
    <link rel="stylesheet" href="{% static 'medicos/css/cadastro_medico.css' %}">
    <link rel="stylesheet" href="{% static 'pacientes/css/home.css' %}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

{% endblock 'head' %}

{% block 'body' %}

    <div class="container">
        <br>
        {% if messages %}
            <br>
            {% for message in messages %}
                <section class="alert {{message.tags}}">
                    {{message}}
                </section>
            {% endfor %}
        {% endif %}
        <h2><span class="color-dark">Suas consultas</span></h2>

        <div class="row">

            <div class="col-md">
                <input type="text" name="especialidades" id="" class="form-control shadow-main-color" placeholder="Especialidades médias">
            </div>
            <div class="col-md">
                <input type="date" name="data" id="" class="form-control shadow-main-color" placeholder="Data da consulta">

            </div>
            <div class="col-md">
                <input type="submit" value="Filtrar" class="btn btn-dark-color-outline">
            </div>
        </div>

        <br>
        
        <h2><span class="color-dark">Hoje</span></h2>
        <div class="list-minhas-consultas">
            <table class="table">
                <thead>
                  <tr>
                    <th scope="col">Paciente</th>
                    <th scope="col">Status</th>
                    <th scope="col">Data</th>
                  </tr>
                </thead>
                <tbody>
                    {% for consulta in consultas_hoje  %}
                        <tr>
                            <td><a href="">{{consulta.paciente}}</a></td>
                            <td>{{consulta.get_status_display}}</td>
                            <td>{{consulta.data_aberta.data}}</td>
                        </tr>
                    {% endfor %}
                </tbody>
              </table>

        </div>

        <hr>
        

        <h2><span class="color-dark">Restantes</span></h2>
        <div class="list-minhas-consultas">
            <table class="table">
                <thead>
                  <tr>
                    <th scope="col">Pacientes</th>
                    <th scope="col">Status</th>
                    <th scope="col">Data</th>
                  </tr>
                </thead>
                <tbody>
                    {% for consulta in consultas_restantes  %}
                        <tr>
                            <td><a href="">{{consulta.paciente}}</a></td>
                            <td>{{consulta.get_status_display}}</td>
                            <td>{{consulta.data_aberta.data}}</td>
                        </tr>
                    {% endfor %}
                </tbody>
              </table>

        </div>

    </div>

{% endblock 'body' %}
```