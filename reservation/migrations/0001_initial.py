import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("app", "0004_merge_models"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("etat", models.CharField(max_length=20, choices=[("en_attente", "En attente"), ("prete", "Prête"), ("empruntee", "Empruntée"), ("rendue", "Rendue"), ("annulee", "Annulée")], default="en_attente")),
                ("date_creation", models.DateField(auto_now_add=True)),
                ("date_modification", models.DateField(auto_now=True)),
                ("emprunteur", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reservations", to=settings.AUTH_USER_MODEL)),
                ("livre", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reservations", to="app.livre")),
            ],
        ),
    ]
