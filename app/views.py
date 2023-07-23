from .forms import Videosform
from .models import Videos

from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    videos = Videos.objects.all()
    return render(request, 'index.html', {'videos':videos})

def admin(request):
    if request.method == 'POST':
        form = Videosform(request.POST, request.FILES) 
        action = request.POST.get('action')
        if action == 'add':
            if form.is_valid():
                video = form.save(commit=False)
                video.nombre = form.cleaned_data['nombre']
                video.descripcion = form.cleaned_data['descripcion']
                video.categoria = form.cleaned_data['categoria']
                video.miniatura = form.cleaned_data['miniatura']
                video.save()
        videos = Videos.objects.all()
        contex = {'videos':videos}
        if action == 'delete':
            video = Videos.objects.get(id=request.POST.get('id'))
            video.delete()
        if action == 'edit':
            video = Videos.objects.get(id=request.POST.get('id'))
            video.nombre = request.POST.get('nombre')
            video.descripcion = request.POST.get('descripcion')
            video.categoria = request.POST.get('categoria')
            video.save()
        return render(request, 'admin.html', contex)
    else:
        videos = Videos.objects.all()
        contex = {'videos':videos}
        return render(request, 'admin.html', contex)
    
def register(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST["email"]).exists():
            msg = "Este email ya existe"
            return render(request, 'register.html', {'msg': msg})
        elif User.objects.filter(username=request.POST["first_name"]).exists():
            msg = "Este username ya existe"
            return render(request, 'register.html', {'msg': msg})
        else:
            afterhashed = request.POST["password"]
            user = User.objects.create_user(email=request.POST["email"],
                                            password=request.POST["password"],
                                            username=request.POST["first_name"],
                                            first_name=request.POST["first_name"],
                                            last_name=request.POST["last_name"])
            user.save()
            userl = authenticate(
                request, username=user.username, password=afterhashed)
            login(request, userl)
            return redirect(index)
    else:
        return render(request, 'register.html')

    
def login_(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = User.objects.filter(Q(username=username) | Q(email=username)).first()
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            msg = 'Datos incorrectos, intente de nuevo'
            return render(request, 'login.html', {'msg':msg})
    else:
        return render(request, 'login.html')
       
def logout_(request):
    logout(request)
    return redirect(index)

def play_(request, id):
    video = Videos.objects.get(id=id)
    return render(request, 'play.html', {'video':video})