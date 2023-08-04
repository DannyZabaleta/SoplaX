from django import forms
from .models import Videos
from django.core.exceptions import ValidationError


class Videosform(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ['nombre', 'descripcion', 'miniatura', 'video', 'categoria']

    def clean_video(self):
        video = self.cleaned_data['video']
        max_size = 524288000  # 500 MB (500 * 1024 * 1024 bytes)

        if video.size > max_size:
            raise ValidationError(f"El tamaño máximo permitido para el archivo de video es de {max_size} bytes (50 MB).")

        return video