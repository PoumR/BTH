from django.urls import path
from .views import (ListeReservationsView, LivresAReserverView, ReserverLivreView,
                    AnnulerReservationView, GestionReservationsView, ChangerEtatReservationView)
app_name = "reservation"
urlpatterns = [
    path("", ListeReservationsView.as_view(), name="liste_reservations"),
    path("livres/", LivresAReserverView.as_view(), name="livres_a_reserver"),
    path("reserver/<int:livre_id>/", ReserverLivreView.as_view(), name="reserver_livre"),
    path("annuler/<int:reservation_id>/", AnnulerReservationView.as_view(), name="annuler_reservation"),
    path("gestion/", GestionReservationsView.as_view(), name="gestion"),
    path("gestion/<int:reservation_id>/etat/", ChangerEtatReservationView.as_view(), name="changer_etat"),
]
