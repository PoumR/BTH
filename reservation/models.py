from django.conf import settings
from django.db import models

class Reservation(models.Model):
    class Etat(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"
        PRETE = "prete", "Prête"
        EMPRUNTEE = "empruntee", "Empruntée"
        RENDUE = "rendue", "Rendue"
        ANNULEE = "annulee", "Annulée"

    ETATS_ACTIFS = (Etat.EN_ATTENTE, Etat.PRETE, Etat.EMPRUNTEE)
    TRANSITIONS_GESTIONNAIRE = {
        Etat.EN_ATTENTE: (Etat.PRETE, Etat.ANNULEE),
        Etat.PRETE: (Etat.EMPRUNTEE, Etat.ANNULEE),
        Etat.EMPRUNTEE: (Etat.RENDUE,),
    }
    TRANSITIONS_ADHERENT = {
        Etat.EN_ATTENTE: (Etat.ANNULEE,),
        Etat.PRETE: (Etat.ANNULEE,),
    }

    emprunteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reservations")
    livre = models.ForeignKey("app.Livre", on_delete=models.PROTECT, related_name="reservations")
    etat = models.CharField(max_length=20, choices=Etat.choices, default=Etat.EN_ATTENTE)
    date_creation = models.DateField(auto_now_add=True)
    date_modification = models.DateField(auto_now=True)

    @property
    def actions_gestionnaire(self):
        return [(etat, self.Etat(etat).label) for etat in self.TRANSITIONS_GESTIONNAIRE.get(self.etat, ())]

    def changer_etat(self, nouvel_etat, gestionnaire=False):
        transitions = self.TRANSITIONS_GESTIONNAIRE if gestionnaire else self.TRANSITIONS_ADHERENT
        if nouvel_etat not in transitions.get(self.etat, ()):
            raise ValueError("Transition non autorisée")
        self.etat = nouvel_etat
        self.save(update_fields=["etat", "date_modification"])
