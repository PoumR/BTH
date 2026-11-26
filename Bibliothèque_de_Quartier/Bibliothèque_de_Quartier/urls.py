from django.contrib import admin
from django.urls import include, path
from catalogue.views import AccueilView

from users.views import (
    CreateInscriptionView,
    ConnexionView,
    CustomLogoutView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", AccueilView.as_view(), name="accueil"),
    path("users/", include("users.urls"),name="users"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('catalogue/', include('catalogue.urls')),
    path('reservation/', include('reservation.urls')),
    path("connexion/", ConnexionView.as_view(), name="connexion"),
    path("deconnexion/", CustomLogoutView.as_view(), name="deconnexion"),
    path("inscription/", CreateInscriptionView.as_view(), name="inscription"),

]
