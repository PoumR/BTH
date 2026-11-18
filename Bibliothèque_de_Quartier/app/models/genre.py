from django.db import models

class Genre(models.Model):
    nom = models.CharField(max_length=50, unique = True)
    
