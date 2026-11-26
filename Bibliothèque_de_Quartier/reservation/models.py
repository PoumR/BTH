from datetime import date

from django.db import models
from django.conf import settings
from catalogue.models.livre import Livre

# Creation Modele Reservation
class Reservation(models.Model):

    class Etat(models.TextChoices):
        EN_ATTENTE = "En attente", "En attente"
        ACCEPTEE = "Acceptée", "Acceptée"
        REFUSEE = "Refusée", "Refusée"
        ANNULEE = "Annulée", "Annulée"

    emprunteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
        related_name = "reservations")

    livre = models.ForeignKey(
            Livre,
            on_delete = models.PROTECT,
            related_name = "reservations")
    
    etat = models.CharField( max_length = 20, choices = Etat.choices, default = Etat.EN_ATTENTE)

    date_creation = models.DateField(default=date.today)
    date_modification = models.DateField(auto_now = True)


    @property
    def actions_gestionnaire(self):
        return [self.Etat(e) for e in self.TRANSITIONS_GESTIONNAIRE.get(self.etat, [])]


    def changer_etat(self, nouvel_etat, gestionnaire=False):

        transitions_autorisees = {
            self.Etat.EN_ATTENTE: [
            self.Etat.ACCEPTEE,
            self.Etat.REFUSEE,
            self.Etat.ANNULEE
        
            ],
            self.Etat.ACCEPTEE: [],
            self.Etat.REFUSEE: [],
            self.Etat.ANNULEE: [],
        }

        if nouvel_etat not in transitions_autorisees.get(self.etat, []):
            raise ValueError("Transition non autorisée.")

        self.etat = nouvel_etat 
        self.save()