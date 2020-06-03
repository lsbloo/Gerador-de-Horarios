from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .forms import LoginForm
from django.shortcuts import redirect
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def create_account_admin(username,password1,password2,email):
    try:
        if password1 != password2:
            caty = 'Passwords não são iguais, por favor checar novamente.'
            return {"caty": caty}
        else:
            users = User.objects.all()
            if len(users) > 1:
                return {"caty": 'Já existe um administrador master, por favor contactar o administrador.'}
            else:
                user = User.objects.create_user(username,email,password1)
                user.is_staff=True
                user.is_superuser=True
                user.save()
                return {"result": True,"user": username}
    except IntegrityError:
        caty = 'Já existe um administrador com este username.'
        return {"caty": caty}

def singup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password1 = form.cleaned_data.get('password1')
            raw_password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            result = create_account_admin(username,raw_password1,raw_password2,email)
            if result.get('result') == True:
                u = authenticate(username=username,password=raw_password1)
                if u is not None:
                    login(request, u)
                    return redirect('/kitkat/dashboard')

            else:
                re = result.get('caty')
                return render(request,'error.html',{'message': re})
    else:
        form = SignUpForm()
    
    return render(request,'singup.html', {'form': form})


@login_required
def logouter(request):
    logout(request)
    return redirect('loginx')



def loginx(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password1 = form.cleaned_data.get('password')
            user = User.objects.get(username=username)
            if user.is_staff:
                u = authenticate(username=username,password=raw_password1)
                if u is not None:
                    login(request,u)
                    return redirect('/kitkat/dashboard')
            else:
                u = authenticate(username=username,password=raw_password1)
                if u is not None:
                    login(request,u)
                    return redirect('/kitkat/dashboard/user')

        else:
            return render(request,'error.html', {'message': "credenciais inválidas."})
    else:
        form = LoginForm()

    return render(request,'login.html', {'form': form})





