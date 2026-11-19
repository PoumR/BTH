from django.db import models
from django.conf import settings

# Creation Modele Reservation
class Reservation(models.Model):
    Emprunteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    Etat = models.CharField(max_length=50)
    Date_Creation = models.DateField(auto_now_add=True)
    Date_Modification = models.DateField(auto_now=True)