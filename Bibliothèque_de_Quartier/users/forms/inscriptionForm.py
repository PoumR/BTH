from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from users.models import Emprunteur

class InscriptionForm(forms.ModelForm):
    
    class Meta:
        model = Emprunteur
        fields = ["nom","prenom","email","password","numero_adherent","role"]

        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "numero_adherent": forms.TextInput(attrs={"class": "form-control"}),
        }

        error_messages = {
            'email': {
                'unique': "Cet email est déjà utilisé.",
            },
        }

