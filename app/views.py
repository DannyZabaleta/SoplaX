import smtplib
import string
import random

from .models import Videos, Usuario

from email.message import EmailMessage

from django.db.models import Q
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.

def user_is_admin(user):
    return user.is_authenticated and user.is_staff

def index(request):
    if request.method == 'GET':
        videos = Videos.objects.all()
        return render(request, 'index.html', {'videos':videos, 'autocomplete':videos})
    else:
        return search(request, request.POST.get('search'))
    
def search(request, txtbusqueda):
    busqueda = Videos.objects.filter(Q(nombre__icontains=txtbusqueda))
    return render(request, 'index.html',{'videos': busqueda, 'autocomplete':Videos.objects.all()})
    
def register(request):
    if request.method == 'POST':
        if Usuario.objects.filter(email=request.POST["email"]).exists():
            msg = "Este email ya existe"
            return render(request, 'register.html', {'msg': msg})
        elif Usuario.objects.filter(username=request.POST["first_name"]).exists():
            msg = "Este username ya existe"
            return render(request, 'register.html', {'msg': msg})
        else:
            afterhashed = request.POST["password"]
            user = Usuario.objects.create_user(email=request.POST["email"],
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
        email = request.POST['email']
        password = request.POST['password']
        usuario = Usuario.objects.filter(Q(email=email)).first()
        if not usuario.is_active and password==usuario.temp_password:
            return activate_user(request, usuario, password)

        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            msg = 'Datos incorrectos, intente de nuevo'
            return render(request, 'login.html', {'msg':msg})
    else:
        return render(request, 'login.html')
    
def activate_user(request, usuario, password):
    if request.POST['newpassword'] == 'True':
        return render(request, 'activateUser.html', {'password':password, 'email':usuario.email})
    else:
        usuario.set_password(request.POST['newpassword'])
        usuario.is_active = True
        usuario.temp_password = ''
        usuario.save()
        return redirect(login_)
        

def recover_password(request):
    email = request.POST.get('email')
    if request.method == 'POST':
        if Usuario.objects.filter(email=email).exists():
            receiver_email_address = email
            email_subject = "Recupera tu contraseña"

            comp = Usuario.objects.get(email=request.POST["email"])
            password = generar_password()
            comp.temp_password = password
            comp.is_active = False
            comp.save()

            print(sendEmail(email_subject, receiver_email_address, "Hola caballero, al parecer usted ha perdido el acceso a nuestra pagina web, este es su contraseña temporal: " + password))

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
    return password

def logout_(request):
    logout(request)
    return redirect(index)

def play_(request, id):
    video = Videos.objects.get(id=id)
    video.visitas += 1
    video.save()
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
    
def redirect_(request):
    return render(request, 'redirect.html')