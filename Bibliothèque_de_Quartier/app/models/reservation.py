"""from django.db import models
from django.conf import settings
from .livre import Livre

# Creation Modele Reservation
class Reservation(models.Model):
    emprunteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    livre = models.ForeignKey(
            Livre,
            on_delete=models.PROTECT,
            related_name="reservations",
        )
    
    etat = models.CharField(max_length=50)
    date_Creation = models.DateField(auto_now_add=True)
    date_Modification = models.DateField(auto_now=True)"""