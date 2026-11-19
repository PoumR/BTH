from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from django.conf import settings
import os
import pandas as pd


# fichier = settings.DATA_DIR / "export.csv"
donnees = ["actions","categories","objets","utilisateurs"]
# fichier = os.path.join(settings.DATA_DIR)

class Command(BaseCommand):
    help = "Description de ma fonction exécutable via manage.py"

    # def add_arguments(self, parser):
    #     parser.add_argument("nom", type=str, help="Argument obligatoire")
    #     parser.add_argument(
    #         "--option",
    #         action="store_true",
    #         help="Option facultative",
    #     )

    def add_arguments(self, parser):
        """Déclare les arguments de la commande.

        Args:
            parser: Parser argparse fourni par Django.
        """
        parser.add_argument("modele", help="Modèle cible, ex. : Genre")
        parser.add_argument("chemin", type=Path, help="Chemin du fichier CSV.")
        parser.add_argument(
            "--key",
            nargs="+",
            default=[],
            help="Colonne(s) identifiant une ligne existante (active la mise à jour).",
        )
        parser.add_argument(
            "--delimiter", default=";", help="Séparateur (défaut : ';')."
        )

    # def add_arguments(self, parser):
    #     """Déclare les arguments de la commande.

    #     Args:
    #         parser: Parser argparse fourni par Django.
    #     """
    #     parser.add_argument("chemin", type=Path, help="Chemin du fichier CSV.")
    #     parser.add_argument(
    #         "--delimiter",
    #         default=";",
    #         help="Séparateur de colonnes (défaut : ';').",
    #     )
    #     parser.add_argument(
    #         "--batch-size",
    #         type=int,
    #         default=1000,
    #         help="Nombre de lignes par requête d'insertion (défaut : 1000).",
    #     )

    def handle(self, *args, **options):

        try:
            modele = apps.get_model(options["modele"])
        except (LookupError, ValueError) as exc:
            raise CommandError(f"Modèle introuvable : {options['modele']}") from exc

        # chemin = options["chemin"]
        # if not chemin.is_file():
        #     raise CommandError(f"Fichier introuvable : {chemin}")

        # for table in donnees:
        #     fichier = os.path.join(settings.DATA_DIR, f"{table}.csv")
        #     # print(fichier)
        #     df = pd.read_csv(fichier)
        #     if table == "categories" or table == "objets":
        #         print(df)
        # with open(fichier as f:
        # if options["option"]:
        #     self.stdout.write(self.style.SUCCESS(f"Bonjour {nom} (option active)"))
        # else:
        #     self.stdout.write(f"Bonjour {nom}")

        # 1. Connect to SQLite database (creates the file if it doesn't exist)
