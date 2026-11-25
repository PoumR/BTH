"""Importer les CSV du brief de manière idempotente.
Usage : python manage.py charger_demo
"""
import csv
from pathlib import Path
from datetime import date
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Genre, Livre
from users.models import Emprunteur
from reservation.models import Reservation

class Command(BaseCommand):
    help = "Charge les catégories, livres, utilisateurs et actions de démonstration."

    def handle(self, *args, **kwargs):
        folder = Path(settings.DATA_DIR)
        def rows(name):
            with (folder/name).open(encoding="utf-8-sig", newline="") as f:
                yield from csv.DictReader(f)
        with transaction.atomic():
            for row in rows("categories.csv"):
                Genre.objects.update_or_create(pk=int(row["id"]), defaults={"nom":row["nom"]})
            for row in rows("objets.csv"):
                Livre.objects.update_or_create(pk=int(row["id"]), defaults={"titre":row["titre"],"auteur":row["auteur"],"annee":int(row["annee"]),"genre_id":int(row["categorie_id"]),"resume":row["resume"],"exemplaires":int(row["exemplaires"]),"isbn":row["isbn"]})
            for row in rows("utilisateurs.csv"):
                defaults={"prenom":row["prenom"],"nom":row["nom"],"email":row["email"],"numero_adherent":row["numero_adherent"],"role":"gestionnaire" if row["role"]=="gestionnaire" else "adhérent"}
                user,created=Emprunteur.objects.update_or_create(pk=int(row["id"]),defaults=defaults)
                if created:
                    user.set_password(settings.DEFAULT_PASSWORD)
                    user.must_change_password=True
                    user.save(update_fields=["password","must_change_password"])
            valid={s.value for s in Reservation.Etat}
            for row in rows("actions.csv"):
                if row["etat"] not in valid:
                    self.stderr.write(f"État ignoré : {row['etat']}")
                    continue
                r,created=Reservation.objects.update_or_create(pk=int(row["id"]), defaults={"emprunteur_id":int(row["utilisateur_id"]),"livre_id":int(row["objet_id"]),"etat":row["etat"]})
                # auto_now/add sinon remplaceraient les dates du fichier CSV
                Reservation.objects.filter(pk=r.pk).update(date_creation=date.fromisoformat(row["date_creation"]),date_modification=date.fromisoformat(row["date_modification"]))
        self.stdout.write(self.style.SUCCESS("CSV importés ; données existantes conservées et mises à jour."))
