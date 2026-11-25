from django.urls import path
from .views import ListeReservationsView
urlpatterns = [path("", ListeReservationsView.as_view(), name="mes_demandes")]
