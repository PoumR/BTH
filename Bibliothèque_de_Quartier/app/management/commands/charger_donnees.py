from pathlib import Path

from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from django.conf import settings
from django.db import IntegrityError, transaction
import csv
import os
import pandas as pd


# fichier = settings.DATA_DIR / "export.csv"
donnees = ["actions","categories","objets","utilisateurs"]
# fichier = os.path.join(settings.DATA_DIR)

class Command(BaseCommand):
    help = "Importe le contenu d'un fichier csv dans la table indiqué"

    def add_arguments(self, parser):
        """Déclare les arguments de la commande.

        Args:
            parser: Parser argparse fourni par Django.
        """
        parser.add_argument("modele", help="Modèle cible (exemple: Genre)")
        parser.add_argument("fichier", type=Path, help="Chemin du fichier CSV.")

    def handle(self, *args, **options):

        try:
            modele = apps.get_model(options["modele"])
        except (LookupError, ValueError) as exc:
            raise CommandError(f"Modèle introuvable : {options['modele']}") from exc

        # print(modele)
        erreurs = []

        # On s'assure que l'insertion ne sera pas incomplète
        with transaction.atomic():
            with open(options["fichier"], encoding="utf-8-sig", newline="") as f:
                lecteur = csv.DictReader(f, delimiter=",")
                print(lecteur)

                for ligne in lecteur:
                    print(ligne)
                    # On reporte les valeurs nulles pour les champs qui l'acceptent
                    for nom, valeur in ligne.items():
                        print(f"{nom}: {valeur}")
                        if valeur == "" and modele._meta.get_field(nom).null:
                            ligne[nom] = None

                    # création de l'instance python
                    objet = modele(**ligne)
                    print(objet)

                    try:
                        # Conversion des attributs dans les bons types
                        objet.full_clean()
                    except ValidationError as exc:
                        erreurs.append(f"Ligne {lecteur.line_num} : {exc.message_dict}")
                        continue

                    # Si des erreurs ont déjà été trouvées, inutile d'écrire :
                    # tout sera annulé de toute façon.
                    if erreurs:
                        continue

                    try:
                        # on sauvegarde en bdd (insert ou update si l'id existe)
                        objet.save()
                    except IntegrityError as exc:
                        # Contrainte refusée par la base elle-même : on arrête.
                        raise CommandError(f"Ligne {lecteur.line_num} : {exc}") from exc

            if erreurs:
                for erreur in erreurs:
                    self.stderr.write(erreur)
                # Lever l'exception ici, dans le bloc atomic, annule tout.
                raise CommandError(
                    f"{len(erreurs)} ligne(s) invalide(s) : import annulé."
                )

        self.stdout.write(self.style.SUCCESS(f"Import réussi dans {modele.__name__}."))
        
