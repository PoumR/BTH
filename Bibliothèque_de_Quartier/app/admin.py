from django.contrib import admin
from .models.genre import Genre
from .models.livre import Livre


#Register your models here.
admin.site.register(Genre)
admin.site.register(Livre)
