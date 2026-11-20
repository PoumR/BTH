from django.urls import path
from .views import ListeUsersView
from . import views

urlpatterns = [
    path('accueil', views.hello_world, name="hello_world"),
    path('liste_emprunteur', ListeUsersView.as_view(), name="liste_users"),
]
