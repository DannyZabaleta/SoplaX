from django import forms
from .models import Videos


class Videosform(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ['nombre', 'descripcion', 'miniatura', 'video', 'categoria']