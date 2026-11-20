from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
#Creation Modele Emprunteur
class Emprunteur(AbstractUser):
    class Roles(models.TextChoices):
        GESTIONNAIRE = "gestionnaire", "Gestionnaire"
        ADHERENT = "adhérent", "Adhérent"
    
    # Supprimer les champs d'origine
    first_name = None
    last_name = None
    username = None
    email = models.EmailField("adresse e-mail", unique=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Créer les nouveaux champs
    prenom = models.CharField("Prénom", max_length=150, blank=False)
    nom = models.CharField("Nom", max_length=150, blank=False)

    
    role = models.CharField(
        max_length=50,
        choices=Roles.choices
    )

    numero_adherent = models.CharField(
        max_length=8,
        unique=True
    )


    objects = CustomUserManager()


