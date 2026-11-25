import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth import views as auth_views
from rich import print

from .forms.inscriptionForm import CustomPasswordChangeForm, InscriptionForm

from .models import Emprunteur


# Create your views here.
def hello_world(request):
    context = {
        "message": "hello world !",
    }
    return render(request=request, template_name="users/index.html", context=context)


class ListeUsersView(ListView):
    model = Emprunteur
    template_name = 'users/liste_users.html'
    context_object_name = "emprunteurs"

    def get_context_data(self, **kwargs):
        # 1. Récupère le contexte de base de la ListView
        context = super().get_context_data(**kwargs)
        
        # 2. Ajoute les données supplémentaires au dictionnaire
        context['titre_page'] = "Tous nos utilisateurs"
        # context['categories'] = Categorie.objects.all()
        # context['total_articles'] = Article.objects.count()
        
        # 3. Retourne le contexte mis à jour
        return context

    def get_queryset(self):
        query = self.request
        print(query)
        print(dir(query))
        return Emprunteur.objects.all()
        # return super().get_queryset()

class CreateInscriptionView(CreateView):
    model = Emprunteur
    form_class = InscriptionForm
    template_name = "users/auth/inscription.html"
    success_url = reverse_lazy("connexion")
    # logging.warning("Rendu: %s", form.as_table())
    
    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)

class ConnexionView(auth_views.LoginView):
    template_name = 'users/auth/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        user = form.get_user()
        return super().form_valid(form)

class CustomLogoutView(auth_views.LogoutView):
    next_page = "users:connexion"

    def post(self, request, *args, **kwargs):
        messages.success(request, "Vous êtes déconnecté.")
        return super().post(request, *args, **kwargs)
