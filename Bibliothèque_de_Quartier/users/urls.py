from django.urls import path
from .views import AccueilUsersView, CreateInscriptionView, ListeUsersView
from . import views
from django.contrib.auth import views as auth_views


app_name = "users"

urlpatterns = [
    path("", AccueilUsersView.as_view(), name="accueil"),
    # path("gestion", ListeUsersView.as_view(), name="liste_users"),
    # --- Auth ---
    # =========================================================================
    path("connexion/", views.ConnexionView.as_view(), name="connexion"),
    path("deconnexion/", views.CustomLogoutView.as_view(), name="deconnexion"),
    path("inscription", CreateInscriptionView.as_view(), name="inscription"),
]
