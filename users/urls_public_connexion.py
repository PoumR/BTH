from django.urls import path
from .views import ConnexionView
urlpatterns = [path("", ConnexionView.as_view(), name="connexion_public")]
