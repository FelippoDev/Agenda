from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso.')
        return redirect('dashboard')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not senha or not senha2 or not usuario:
        messages.error(request, 'Nenhum campo pode estar vazio.')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)

    except:
        messages.error(request, 'Email Inválido.')
        return render(request, 'accounts/register.html')

    if len(usuario) < 6:
        messages.error(request, 'Nome de usuário inválido.')
        return render(request, 'accounts/register.html')

    if len(senha) < 5 and len(senha2) < 5:
        messages.error(request, 'Senha inválida, precisa ter 5 caracteres ou mais')
        return render(request, 'accounts/register.html')

    if senha != senha2:
        messages.error(request, 'Senhas diferentes.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Nome de usuário já existente.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Endereço de e-mail já existente.')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Registrado com sucesso!')
    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    nome = request.POST.get('nome')

    form.save()
    messages.success(request, f'Contato {nome} salvo com sucesso!')
    return redirect('dashboard')
