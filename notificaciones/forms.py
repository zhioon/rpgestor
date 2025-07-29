# notificaciones/forms.py

from django import forms
from .models import InternalMessage

class InternalMessageForm(forms.ModelForm):
    class Meta:
        model = InternalMessage
        fields = ['recipient','subject','body']
        labels = {
            'recipient': 'Destinatario',
            'subject':   'Asunto',
            'body':      'Cuerpo del mensaje',
        }
        widgets = {
          'body': forms.Textarea(attrs={'rows':4, 'cols':40})
        }
