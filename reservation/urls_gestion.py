from django.urls import path
from .views import GestionReservationsView
urlpatterns = [path("", GestionReservationsView.as_view(), name="gestion_public")]
