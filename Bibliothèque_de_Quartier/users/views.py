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
        "message": "hello world !",
        "message": "hello world !",
        "message": "hello world !",
    }
    return render(request=request,template_name="users/index.html",context=context)

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
    template_name = "users/inscription.html"
    success_url = reverse_lazy("login")
    # logging.warning("Rendu: %s", form.as_table())

class ConnexionView(auth_views.LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('users:liste_users')

    def form_valid(self, form):
        user = form.get_user()
        if user.must_change_password:
            return HttpResponseRedirect(reverse('password_change'))
        return super().form_valid(form)


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "registration/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.user.must_change_password = False
        self.request.user.save()
        return response


class CustomLogoutView(auth_views.LogoutView):
    next_page = "users:login"

    def post(self, request, *args, **kwargs):
        messages.success(request, "Vous êtes déconnecté.")
        return super().post(request, *args, **kwargs)
