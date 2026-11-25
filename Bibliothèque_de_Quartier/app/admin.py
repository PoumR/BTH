from django.contrib import admin
from .models.genre import Genre
from .models.livre import Livre
from .models.emprunteur import Emprunteur


#Register your models here.
admin.site.register(Emprunteur)
admin.site.register(Genre)
admin.site.register(Livre)
