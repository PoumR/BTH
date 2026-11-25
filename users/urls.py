from django.urls import path
from .views import AccueilUsersView, CreateInscriptionView, ConnexionView, CustomLogoutView, ListeUsersView

app_name = "users"
urlpatterns = [
    path("", AccueilUsersView.as_view(), name="accueil"),
    path("accueil", AccueilUsersView.as_view(), name="accueil_ancien"),
    path("connexion/", ConnexionView.as_view(), name="connexion"),
    path("deconnexion/", CustomLogoutView.as_view(), name="deconnexion"),
    path("inscription/", CreateInscriptionView.as_view(), name="inscription"),
    path("gestion/", ListeUsersView.as_view(), name="liste_users"),
]
