from django import forms
from users.models import Emprunteur

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        fields = ["nom","prenom","numero_adherent","email","password","role"]

        # widgets = {
        #     "nom": forms.TextInput(attrs={"class": "form-control"}),
        #     "nom": forms.TextInput(attrs={"class": "form-control"}),
        #     "nom": forms.TextInput(attrs={"class": "form-control"}),
        #     "nom": forms.TextInput(attrs={"class": "form-control"}),
        #     "nom": forms.TextInput(attrs={"class": "form-control"}),
        #     "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        # }
