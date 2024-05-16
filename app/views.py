from django.shortcuts import render, redirect
from app.models import Client
from app.forms import ClientForm

# Create your views here.
def addClient(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect(listClient)
        else:
            return render(request, 'addClient.html', {'msg':'Completa correctamente todos los campos.'})
    else:
        return render(request, 'addClient.html')

def listClient(request):
    list = Client.objects.all()
    return render(request, 'listClient.html', {'list':list})

def deleteClient(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect(listClient)

def editClient(request, id):
    client = Client.objects.get(id=id)
    if request.method == 'POST':
        client.name = request.POST["name"]
        client.phone = request.POST["phone"]
        client.message1 = request.POST["message1"]
        client.message2 = request.POST["message2"]
        client.message3 = request.POST["message3"]
        client.message4 = request.POST["message4"]
        client.save()
        return redirect(listClient)
    else:
        return render(request, 'editClient.html', {'client':client})