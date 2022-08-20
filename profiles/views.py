from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UpdateProfileForm
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

def perfil(request, pk):
    perfil_usuario = UserProfile.objects.get(id_perfil=pk)
    context = {'perfil': perfil_usuario}
    return render(request, 'profiles/profile.html', context)

def conta(request):
    conta_usuario = request.user.userprofile
    context = {'conta': conta_usuario}
    return render(request, 'profiles/account.html', context)


def criarperfil(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="profiles/createprofile.html", context={"register_form":form})

    
def logarperfil(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario != None:
            login(request, usuario)
            return redirect('index')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'profiles/login.html', {'form_login': form_login})

def deslogarperfil(request):
    logout(request)
    return redirect('index')

def atualizarperfil(request):
    perfil = request.user.userprofile
    form = UpdateProfileForm(instance=perfil)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.info(request, 'Você atualizou seu perfil!')
            return redirect('index')
    context = {"form": form}
    return render(request, 'profiles/updateprofile.html', context)

def deletarperfil(request):
    perfil = request.user.userprofile
    form = UpdateProfileForm(instance=perfil)
    if request.method == 'POST':
        user = request.user
        user.delete()

        return redirect('index')
    context = {"form": form}
    return render(request, 'profiles/deleteprofile.html', context)
