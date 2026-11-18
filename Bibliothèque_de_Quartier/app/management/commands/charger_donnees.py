from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Description de ma fonction exécutable via manage.py"

    def add_arguments(self, parser):
        parser.add_argument("nom", type=str, help="Argument obligatoire")
        parser.add_argument(
            "--option",
            action="store_true",
            help="Option facultative",
        )

    def handle(self, *args, **options):
        nom = options["nom"]
        if options["option"]:
            self.stdout.write(self.style.SUCCESS(f"Bonjour {nom} (option active)"))
        else:
            self.stdout.write(f"Bonjour {nom}")