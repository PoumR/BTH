from django.shortcuts import render
from django.views.generic import ListView
from rich import print

from .models import Emprunteur

# Create your views here.
def hello_world(request):
    context = {
        "message": "hello world !",
    }
    return render(request=request,template_name="users/index.html",context=context)

class ListeUsersView(ListView):
    model = Emprunteur
    template_name = 'users/liste_users.html'
    context_object_name = "emprunteurs"

    def get_queryset(self):
        query = self.request
        print(query)
        print(dir(query))
        return Emprunteur.objects.all()
        # return super().get_queryset()
