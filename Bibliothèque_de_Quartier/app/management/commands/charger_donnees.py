from django.core.management.base import BaseCommand

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

    def handle(self, *args, **options):
        for table in donnees:
            fichier = os.path.join(settings.DATA_DIR, f"{table}.csv")
            # print(fichier)
            df = pd.read_csv(fichier)
            print(df)
            # with open(fichier as f:
        # if options["option"]:
        #     self.stdout.write(self.style.SUCCESS(f"Bonjour {nom} (option active)"))
        # else:
        #     self.stdout.write(f"Bonjour {nom}")