from django.urls import path
from . import views

app_name = "reservation"

urlpatterns = [
    path('', views.ListeReservationsView.as_view(), name='liste_reservations'),
    path('livres/', views.LivresAReserverView.as_view(), name='livres_a_reserver'),
    path('reserver/<int:livre_id>/', views.ReserverLivreView.as_view(), name='reserver_livre'),
    path('annuler/<int:reservation_id>/', views.AnnulerReservationView.as_view(), name='annuler_reservation'),
    path('gestion/', views.GestionReservationsView.as_view(), name='gestion'),
    path('gestion/<int:reservation_id>/etat/', views.ChangerEtatReservationView.as_view(), name='changer_etat'),
]

"""
from django.urls import path, include
from . import views

app_name = "reservation"

urlpatterns = [
    path('', views.liste_reservations, name = 'liste_reservations'),
    path('livres/', views.livres_a_reserver, name='livres_a_reserver'),
    path("reserver/<int:livre_id>/", views.reserver_livre, name="reserver_livre"),
    path("annuler/<int:reservation_id>/", views.annuler_reservation, name="annuler_reservation"),
    path("gestion/", views.gestion_reservations, name="gestion"),
    path("gestion/<int:reservation_id>/changer-etat/", views.changer_etat_reservation, name="changer_etat"),

]
"""