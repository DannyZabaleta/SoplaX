from django.shortcuts import render
from .forms import Videosform
from .models import Videos

# Create your views here.

def index(request):
    videos = ['video1', 'video2', 'video3', 'video4']
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