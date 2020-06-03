from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import CriterionForm
from .forms import KitKatUserForm
from .models import Criterion
from .models import KitKatUser
from django.db.utils import IntegrityError


from django.http import HttpResponseRedirect


def index(request):
    return HttpResponse("URL Indisponivel ;]")

@login_required
def painel_users(request):
    users_kit = KitKatUser.objects.all()
    if len(users_kit) == 0 or users_kit == None:
        return render(request,'dashboard_user.html',context=None)
    else:
         return render(request,'dashboard_user.html',context={"users_list": users_kit})

@login_required
def painel_user(request):
    return render(request,'dashboard_u.html',context=None)


@login_required
def painel(request):
    criterios = Criterion.objects.all()
    if len(criterios) == 0 or criterios == None:
        return render(request,'dashboard.html',context=None)
    else:
        return render(request,'dashboard.html',context={"criterios_list" : criterios})


@login_required
def painelc(request, slug):
    return render(request,'dashboard.html',context=slug)


def check_rate(rate):
    switcher = {
        10: "Soft Constraint",
        1000:"Hard Constraint",
    }
    return switcher.get(int(rate))

def create_user(username,password,email,is_staff):
    try:
        if is_staff:
            user = User.objects.create_user(username,email,password)
            user.is_staff=True
            user.is_superuser=True
            user.save()

            kit_kat_user = KitKatUser.objects.create(username=username,password=password,email=email,is_staff=is_staff)
            kit_kat_user.save()
            return True
        else:
            user = User.objects.create_user(username,email,password)
            user.is_staff=False
            user.is_superuser=False
            user.save()
            kit_kat_user = KitKatUser.objects.create(username=username,password=password,email=email,is_staff=False)
            kit_kat_user.save()
            return True
    except IntegrityError:
        caty = 'Já existe um usuário com este username.'
        return {"caty": caty}

@login_required
def generate_user(request):
    if request.method =="POST":
        form = KitKatUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            is_staff = form.cleaned_data.get('is_staff')
            res = create_user(username,password,email,is_staff)
            if res:
                return HttpResponseRedirect('/kitkat/dashboard/users/?message=created')
            else:
                return render(request,'error.html',{"message": res.get('caty')})
    return HttpResponseRedirect('/kitkat/dashboard/users/')


@login_required
def generate(request):
    if request.method == "POST":
        form = CriterionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            rate = form.cleaned_data.get('rate')
            constraint = check_rate(rate)
            cr = Criterion.objects.create(name=name,description=description,rate=rate,constraint=constraint)
            cr.save()
            return HttpResponseRedirect('/kitkat/dashboard?message=created')
    else:
        form = CriterionForm()
    
    return render(request,'dashboard.html', {'form': form})

@login_required
def delete_user(request,pk):
    user = KitKatUser.objects.get(id=pk)
    user.delete()
    return HttpResponseRedirect('/kitkat/dashboard/users/?message=deleted')

@login_required
def remove_criterio(request,pk):
    c = Criterion.objects.get(id=pk)
    c.delete()
    return HttpResponseRedirect('/kitkat/dashboard?message=deleted')

@login_required
def edit_criterio(request,pk):
    c = Criterion.objects.get(id=pk)

    return render(request,"edit.html",{"object": c})


@login_required
def edit_criterio_p(request,pk):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        rate = request.POST.get('rate')
        constraint = check_rate(rate)
        criterio = Criterion.objects.get(id=pk)
        criterio.name = name
        criterio.description = description
        criterio.rate=rate
        criterio.constraint = constraint
        criterio.save()
        return HttpResponseRedirect('/kitkat/dashboard?message=edited')
    else:
        return HttpResponseRedirect('/kitkat/dashboard')



            

