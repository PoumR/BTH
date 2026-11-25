from django.urls import path
from .views import ListeLivresView, LivreDetailView
from reservation.views import ReserverLivreView

urlpatterns = [
    path("", ListeLivresView.as_view(), name="liste_livres"),
    path("<int:pk>/", LivreDetailView.as_view(), name="detail_livre"),
    path("<int:pk>/demande/", ReserverLivreView.as_view(), name="demande_livre"),
]
