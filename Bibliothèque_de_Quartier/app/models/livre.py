from django.db import models
from .genre import Genre
from django.core.validators import MinValueValidator, MaxValueValidator


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    annee = models.IntegerField(max_length=4, validators=[ MinValueValidator(1850) , MaxValueValidator(2025) ])
    resume = models.TextField()
    exemplaires = models.IntegerField(validators=[ MinValueValidator(1) , MaxValueValidator(4) ])
    isbn = models.CharField(max_length=13, unique = True)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="livres",
    )




