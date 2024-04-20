# Aula 3

Link para o Notion:

```jsx
https://grizzly-amaranthus-f6a.notion.site/Aula-3-ac3ab8f1e29f4de79b4e5372f59a275e?pvs=4
```

## Navbar

Vamos criar uma barra de navegação.

Para isso crie um arquivo em /templates/partials/navbar.html

```html
{% load static %}
<nav class="navbar navbar-expand-lg navbar-dark bg-color-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#"><img src="{% static 'geral/img/logo.png' %}" width="20%" alt="">&nbspHEALING</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Área do paciente
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                  <li><a class="dropdown-item" href="{% url 'home' %}">Home</a></li>
                  <li><a class="dropdown-item" href="{% url 'minhas_consultas' %}">Minhas consultas</a></li>
                </ul>
            </li>

            {% if is_medico %}
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Área do médico
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                        <li><a class="dropdown-item" href="{% url 'abrir_horario' %}">Abrir horários</a></li>
                        <li><a class="dropdown-item" href="{% url 'consultas_medico' %}">Suas consultas</a></li>
                    </ul>
                </li>
            {% else %}
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'cadastro_medico' %}">Sou médico</a>
                </li>
            {% endif %}
        </ul>
      </div>
    </div>
  </nav>
```

Em todos os HTML adicione a navbar:

```html
{% include "partials/navbar.html" %}
```

Adicione o is_medico no context de todas as views:

```html
'is_medico': is_medico(request.user)
```

## Acessar consulta (Paciente)

Crie uma URL para o paciente acessar a consulta agendada:

```python
path('consulta/<int:id_consulta>/', views.consulta, name="consulta"),
```

Crie a view para consulta:

```python
def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user)
        return render(request, 'consulta.html', {'consulta': consulta, 'dado_medico': dado_medico, 'is_medico': is_medico(request.user)})

```

Agora o consulta.html:

```html
{% extends "base.html" %}
{% load static %}

{% block 'head' %}

    <link rel="stylesheet" href="{% static 'medicos/css/abrir_horario.css' %}">
    <link rel="stylesheet" href="{% static 'usuarios/css/usuarios.css' %}">
    <link rel="stylesheet" href="{% static 'medicos/css/cadastro_medico.css' %}">
    <link rel="stylesheet" href="{% static 'pacientes/css/home.css' %}">
    <link rel="stylesheet" href="{% static 'pacientes/css/agendar_horario.css' %}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

{% endblock 'head' %}

{% block 'body' %}
    {% include "partials/navbar.html" %}

    <br><br>
    <div class="container">
        <div class="row">
            <div class="col-md-8">
                <div class="row">
                    <div class="col-md-3"><img src="{{dado_medico.foto.url}}" class="foto-perfil-card-lg" alt=""></div>
                    <div class="col-md">
                        <p style="font-size: 20px" class="p-bold">Dr(a). {{dado_medico.nome}} <i class="bi bi-patch-check-fill icon-main"></i></p>
                        <p>{{dado_medico.descricao}}</p>
                        <p class="p-bold">{{consulta.data_aberta.data}}</p>
                    </div>
                </div> 
                <hr>
                <br>
                <div class="row">
                    <div class="col-md">
                        
                        <p><i class="color-dark bi bi-check-circle-fill"></i> Consulta agendada</p>
                    </div>
                    <div class="col-md">
                        <p><i class=" bi bi-check-circle-fill"></i> Consulta realizada</p>
                    </div>
                    <div class="col-md">
                        <p><i class="bi bi-check-circle-fill"></i> Consulta Avaliada</p>
                    </div>
                </div>
                <hr>
                <h3 class="p-bold">Detalhes da consulta</h3>
                <p style="font-size:20px"><i class="bi bi-calendar3 color-dark"></i>&nbsp {{consulta.data_aberta.data}}</p>
                <p style="font-size:20px"><i class="bi bi-tag-fill color-dark"></i></i>&nbsp R$ {{dado_medico.valor_consulta}}</p>
                <a style="cursor: auto;" class="btn btn-dark-color-outline btn-lg">Adicione em seu calendário!</a>
                <hr>
                <h3 class="p-bold">Como acessar ?</h3>
                <p>No horário da consulta acesse o link disponível abaixo</p>

                
                <a href="#" class="btn btn-success btn-dark-color btn-lg disabled" >Acessar consulta</a>

                
                <hr>
                <h3 class="p-bold">Meus documentos</h3>
                <br>
    
                <br>
                <br>
                <br>
                <br>
            </div>
            <div class="col-md"></div>
        </div>
        
    </div>

{% endblock 'body' %}
```

Em minhas consultas redirecione para a consulta clicada:

```html
{% url 'consulta' consulta.id %}
```

Adicione uma mensagem informando o status da consulta:

```html
{% if consulta.status == 'C' %}
    <div class="alert alert-danger" role="alert">
        Consulta cancelada
    </div>
{% elif consulta.status == 'F' %}
    <div class="alert alert-success" role="alert">
        Consulta Finalizada
    </div>
{% elif consulta.status == 'I' %}
    <div class="alert alert-primary" role="alert">
        Consulta inicializada, acesse o link imediatamente!
    </div>
{% endif %}
```

Se a consulta já tiver sido realizado altera o consulta realizada para verde:

```html
{% if consulta.status == 'F' %}color-dark{% endif %}
```

Se a consulta já tiver sido iniciado adicione um botão para o paciente acessar a vídeo chamada:

```html
{% if consulta.status == 'I' and consulta.link %}
    <a href="{{consulta.link}}"  class="btn btn-success btn-dark-color btn-lg" >Acessar consulta</a>
{% else %}

    <a href="#"  class="btn btn-success btn-dark-color btn-lg disabled" >Acessar consulta</a>

{% endif %}
```

## Acessar consulta (Médico)

Crie uma URL para o médico pode acessar sua consulta:

```python
path('consulta_area_medico/<int:id_consulta>/', views.consulta_area_medico, name="consulta_area_medico"),
```

Crie a view para o consulta_area_medico:

```python
def consulta_area_medico(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    

    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)
        return render(request, 'consulta_area_medico.html', {'consulta': consulta,'is_medico': is_medico(request.user)}) 
```

Crie o HTML consulta_area_medico.html:

```python
{% extends "base.html" %}
{% load static %}

{% block 'head' %}

    <link rel="stylesheet" href="{% static 'medicos/css/abrir_horario.css' %}">
    <link rel="stylesheet" href="{% static 'usuarios/css/usuarios.css' %}">
    <link rel="stylesheet" href="{% static 'medicos/css/cadastro_medico.css' %}">
    <link rel="stylesheet" href="{% static 'pacientes/css/home.css' %}">
    <link rel="stylesheet" href="{% static 'pacientes/css/agendar_horario.css' %}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

{% endblock 'head' %}

{% block 'body' %}
    {% include "partials/navbar.html" %}

    <br><br>
    <div class="container">
        <div class="row">
            <div class="col-md-8">
                {% if consulta.status == 'C' %}
                    <div class="alert alert-danger" role="alert">
                        Consulta cancelada
                    </div>
                {% elif consulta.status == 'F' %}
                    <div class="alert alert-success" role="alert">
                        Consulta Finalizada
                    </div>
                {% elif consulta.status == 'I' %}
                    <div class="alert alert-primary" role="alert">
                        Consulta inicializada, acesse o link imediatamente!
                    </div>
                {% endif %}
                {% if messages %}
                    <br>
                    {% for message in messages %}
                        <section class="alert {{message.tags}}">
                            {{message}}
                        </section>
                    {% endfor %}
                {% endif %}
                <div class="row">
                    <div class="col-md">
                        <p style="font-size: 20px" class="p-bold">Paciente {{consulta.paciente.username}} <i class="bi bi-patch-check-fill icon-main"></i></p>
                        <p>{{dado_medico.descricao}}</p>
                        <p class="p-bold">{{consulta.data_aberta.data}}</p>
                    </div>
                </div> 
                <hr>
                <br>
                <div class="row">
                    <div class="col-md">
                        
                        <p><i class="color-dark bi bi-check-circle-fill"></i> Consulta agendada</p>
                    </div>
                    <div class="col-md">
                        <p><i class="{% if consulta.status == 'F' %}color-dark{% endif %} bi bi-check-circle-fill"></i> Consulta realizada</p>
                    </div>
                    <div class="col-md">
                        <p><i class="bi bi-check-circle-fill"></i> Consulta Avaliada</p>
                    </div>
                </div>
                <hr>
                <h3 class="p-bold">Detalhes da consulta</h3>
                <p style="font-size:20px"><i class="bi bi-calendar3 color-dark"></i>&nbsp {{consulta.data_aberta.data}}</p>
                <a style="cursor: auto;" class="btn btn-dark-color-outline btn-lg">Adicione em seu calendário!</a>
                <hr>
                <h3 class="p-bold">Como acessar ?</h3>
                <p>Adicione o link do google meet para iniciar a consulta</p>
                <form action="" method="POST">{% csrf_token %}
                    <input type="text" name="link" class="form-control shadow-main-color" id="" placeholder="Link ..." value="">
                    <br>
                    <input type="submit" class="btn btn-success btn-dark-color btn-lg">
                </form>
                
                
                    
                <hr>
                
                <br>
                <br>
                <br>
                <br>
            </div>
            <div class="col-md">
                <h3 class="p-bold">Documentos do paciente</h3>
                <form action="" method="POST" enctype="multipart/form-data">
                    <input type="text" name="titulo" class="form-control" placeholder="Titulo ...">
                    <br>
                    <input type="file" name="documento" class="form-control">
                    <br>
                    <input type="submit" class="btn btn-dark-color-outline btn-lg" value="+">
                </form>
                <hr>
                <br>
                
                <hr>
                <a href="" class="btn btn-primary">Finalizar consulta</a>
            </div>
        </div>
        
    </div>

{% endblock 'body' %}
```

Na aba minhas consultas do médico redirecione para a consulta clicada:

```python
{% url 'consulta_area_medico' consulta.id %}
```

No forms para adicionar o link da consulta redirecione para:

```python
{% url 'consulta_area_medico' consulta.id %}
```

E caso já exista um link o exiba no input:

```python
{% if consulta.link %}{{consulta.link}}{% endif %}
```

Na view consulta_area_medico inicie a consulta:

```python
def consulta_area_medico(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    

    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)
        return render(request, 'consulta_area_medico.html', {'consulta': consulta,'is_medico': is_medico(request.user)}) 
    elif request.method == "POST":
        # Inicializa a consulta + link da chamada
        consulta = Consulta.objects.get(id=id_consulta)
        link = request.POST.get('link')

        *if cons*ulta.status == 'C':
            messages.add_message(request, constants.WARNING, 'Essa consulta já foi cancelada, você não pode inicia-la')
            return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
        elif consulta.status == "F":
            messages.add_message(request, constants.WARNING, 'Essa consulta já foi finalizada, você não pode inicia-la')
            return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
        
        consulta.link = link
        consulta.status = 'I'
        consulta.save()

        messages.add_message(request, constants.SUCCESS, 'Consulta inicializada com sucesso.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
```

## Documentos

Crie uma model para salvar os documentos:

```python
class Documento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=30)
    documento = models.FileField(upload_to='documentos')

    def __str__(self):
        return self.titulo
```

Execute as migrações!

Crie uma URL para o médico adicionar documentos:

```python
path('add_documento/<int:id_consulta>/', views.add_documento, name="add_consulta"),
```

Crie a view add_documento:

```python
def add_documento(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    
    consulta = Consulta.objects.get(id=id_consulta)
    
    if consulta.data_aberta.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua!')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
    
    titulo = request.POST.get('titulo')
    documento = request.FILES.get('documento')

    if not documento:
        messages.add_message(request, constants.WARNING, 'Adicione o documento.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

    documento = Documento(
        consulta=consulta,
        titulo=titulo,
        documento=documento

    )

    documento.save()

    messages.add_message(request, constants.SUCCESS, 'Documento enviado com sucesso!')
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
```

No forms de add documento redirecione para a view criada acima:

```python
{% url 'add_consulta' consulta.id %}
```

Agora vamos listar os documentos criados, primeiro busque na views e envie para o context:

```python
documentos = Documento.objects.filter(consulta=consulta)
return render(request, 'consulta_area_medico.html', {'consulta': consulta, 'documentos': documentos,'is_medico': is_medico(request.user)}) 
```

Agora é só listar no HTML

```python
<a href="{{documento.documento.url}}" class="link documentos"><i class="bi bi-file-arrow-down"></i> {{documento.titulo}} - {{documento.consulta.data_aberta.data.year}}</a>
```

Agora repita o processo e liste os documentos na aba do paciente:

## Python Full

Conheça nosso curso completo de Python e Django que te da acesso à:

- Mais de 630 aulas
- Agendamento de reuniões com professores
- Análises de códigos
- Eventos entre alunos
- Exercícios automáticos
- E muito mais

Para quem participou da PSW 9.0 terá um desconto especial, confira no link abaixo:

https://youtu.be/b0XdgJFqQZM