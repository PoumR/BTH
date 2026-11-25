from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from .forms.inscriptionForm import InscriptionForm
from .models import Emprunteur

class AccueilUsersView(TemplateView):
    template_name = "users/index.html"

class ListeUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Emprunteur
    template_name = "users/liste_users.html"
    context_object_name = "emprunteurs"

    def test_func(self):
        u = self.request.user
        return u.is_staff or u.is_superuser or u.role == Emprunteur.Roles.GESTIONNAIRE

class CreateInscriptionView(CreateView):
    model = Emprunteur
    form_class = InscriptionForm
    template_name = "users/auth/inscription.html"
    success_url = reverse_lazy("users:connexion")

    def form_valid(self, form):
        form.instance.role = Emprunteur.Roles.ADHERENT
        return super().form_valid(form)

class ConnexionView(auth_views.LoginView):
    template_name = "users/auth/login.html"
    redirect_authenticated_user = True

class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("accueil")
