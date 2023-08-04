import smtplib
import string
import random

from .forms import Videosform
from .models import Videos

from email.message import EmailMessage

from django.db.models import Q
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

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
                video.video = form.cleaned_data['video']
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
        print(make_password(password)==usuario.password)
        if not usuario.is_active and make_password(password)==usuario.password:
            print("UwU")

        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            msg = 'Datos incorrectos, intente de nuevo'
            return render(request, 'login.html', {'msg':msg})
    else:
        return render(request, 'login.html')
    
def activate_user(request, usuario):
    if request.method == 'POST':
        usuario.set_password(request.POST['password1'])
        usuario.is_active = True
        usuario.save()
        return redirect(login_)
    else:
        return render(request, 'activateUser.html')

def recover_password(request):
    email = request.POST.get('email')
    if request.method == 'POST':
        if User.objects.filter(email=email).exists():
            receiver_email_address = email
            email_subject = "Recupera tu contraseña"

            comp = User.objects.get(email=request.POST["email"])
            passhashed, cpassword = generar_password()
            comp.password = passhashed
            comp.is_active = False
            comp.save()

            print(sendEmail(email_subject, receiver_email_address, "Hola caballero, al parecer usted ha perdido el acceso a nuestra pagina web, este es su contraseña temporal: " + cpassword))

            request.session['msg'] = "Se envio su nueva contraseña via correo, revise su bandeja"
            return redirect(login_)
        else:
            msg = "Este email no esta registrado a nuestra pagina"
        return render(request, "recoverPassword.html", {'msg':msg})
    else:
        return render(request, "recoverPassword.html")
       
def generar_password(longitud=8):
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres)
                    for i in range(longitud))
    passhashed = make_password(password)
    return passhashed, password

def logout_(request):
    logout(request)
    return redirect(index)

def play_(request, id):
    video = Videos.objects.get(id=id)
    return render(request, 'play.html', {'video':video, 'url':video.video.url})

def sendEmail(subject: str, receiverEmail: str, content: str) -> bool:
    try:
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = settings.SENDER_EMAIL_ADDRESS
        message['To'] = receiverEmail
        message.set_content(content)
        server = smtplib.SMTP(settings.STMPURL, '587')
        server.ehlo()
        server.starttls()
        server.login(settings.SENDER_EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(message)
        server.quit()
        return True
    except:
        return False