from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password

from django.db import transaction
import tablib

from app.resources import get_resource_for_model


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
        fichier = options["fichier"]

        # On s'assure que l'insertion ne sera pas incomplète
        with transaction.atomic():
            self.stdout.write(f"Import de {modele.__name__} depuis {fichier}...")

            # On récupère la bonne ressource
            resource = get_resource_for_model(modele)
            print(resource)

            # On charge le CSV
            dataset = tablib.Dataset()
            with open(fichier,'r',encoding='utf-8') as f:
                dataset.load(f.read(),format='csv',delimiter=',')

            # Import du fichier (avec levée d'erreur)
            resultat = resource.import_data(dataset,dry_run=False,raise_errors=True)
            
            # if modele._meta.model_name == 'user':
            #     hashed = make_password(settings.DEFAULT_PASSWORD)
            #     modele.objects.filter(password='').update(password=hashed)

            # === C'EST ICI QUE VOUS AJOUTEZ LE HASH ===
            if "password" in [f.name for f in modele._meta.get_fields()]:
                hashed = make_password(settings.DEFAULT_PASSWORD)
                modele.objects.filter(password="").update(
                    password=hashed,
                    must_change_password=True
                )

            self.stdout.write(self.style.SUCCESS(f"-> {resultat.total_rows} lignes importées."))