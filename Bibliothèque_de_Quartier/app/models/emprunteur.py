from django.db import models
from django.contrib.auth.models import AbstractUser

#Creation Modele Emprunteur
class Emprunteur(AbstractUser):
    class Roles(models.TextChoices):
        GESTIONNAIRE = "gestionnaire", "Gestionnaire"
        ADHERENT = "adhérent", "Adhérent"
    # Supprimer les champs d'origine
    first_name = None
    last_name = None



    # Créer les nouveaux champs
    prenom = models.CharField("Prénom", max_length=150, blank=False)
    nom = models.CharField("Nom", max_length=150, blank=False)

    
    Role = models.CharField(
        max_length=50,
        choices=Roles.choices
    )

    NumeroAdherent = models.CharField(
        max_length=8,
        unique=True
    )


