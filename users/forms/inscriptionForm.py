from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Emprunteur

class InscriptionForm(UserCreationForm):
    class Meta:
        model = Emprunteur
        fields = ("prenom", "nom", "email", "numero_adherent", "password1", "password2")
        widgets = {
            "prenom": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "nom": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }

class CustomPasswordChangeForm(forms.Form):
    pass
