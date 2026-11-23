import logging

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from rich import print

from .forms.inscriptionForm import InscriptionForm

from .models import Emprunteur

# Create your views here.
def hello_world(request):
    context = {
        "message": "hello world !",
    }
    return render(request=request,template_name="users/index.html",context=context)

class ListeUsersView(ListView):
    model = Emprunteur
    template_name = 'users/liste_users.html'
    context_object_name = "emprunteurs"

    def get_queryset(self):
        query = self.request
        print(query)
        print(dir(query))
        return Emprunteur.objects.all()
        # return super().get_queryset()

class CreateInscriptionView(CreateView):
    model = Emprunteur
    form_class = InscriptionForm
    template_name = "users/inscription.html"
    success_url = reverse_lazy("liste_emprunteur")
    # logging.warning("Rendu: %s", form.as_table())
