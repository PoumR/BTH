from django.db import models
from .genre import Genre

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    année = models.IntegerField(max_length=4)
    resume = models.TextField()
    exemplaires = models.IntegerField(max_length=4)
    isbn = models.CharField(max_length=13)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="livres",
    )