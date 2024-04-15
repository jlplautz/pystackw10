from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import redirect, render


# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(
                request,
                constants.ERROR,
                'Já existe um usuário com o mesmo username',
            )
            return redirect('/usuarios/cadastro')

        if senha != confirmar_senha:
            messages.add_message(
                request, constants.ERROR, 'As senhas não coincídem'
            )
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            messages.add_message(
                request,
                constants.ERROR,
                'A senha deve possuir pelo menos 6 caracteres',
            )
            print('Erro 3')
            return redirect('/usuarios/cadastro')

        try:
            User.objects.create_user(
                username=username, email=email, password=senha
            )
            messages.add_message(
                request, constants.ERROR, 'Usuário cadastrado com sucesso.'
            )
            return redirect('/usuarios/login')
        except:
            messages.add_message(
                request, constants.ERROR, 'Erro interno do sistema'
            )

            return redirect('/usuarios/cadastro')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('/pacientes/home')

        messages.add_message(
            request, constants.ERROR, 'Usuário ou senha incorretos'
        )
        return redirect('/usuarios/login')


def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')
