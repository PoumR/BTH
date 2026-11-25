from django.contrib import admin
from django.urls import include, path
from catalogue.views import AccueilView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", AccueilView.as_view(), name="accueil"),
    path("catalogue/", include("catalogue.urls")),
    path("users/", include("users.urls")),
    path("reservation/", include("reservation.urls")),
    # Routes simples prévues par le brief, réutilisant les mêmes vues.
    path("inscription/", include("users.urls_public_inscription")),
    path("connexion/", include("users.urls_public_connexion")),
    path("deconnexion/", include("users.urls_public_deconnexion")),
    path("mes-demandes/", include("reservation.urls_mes_demandes")),
    path("gestion/", include("reservation.urls_gestion")),
]
