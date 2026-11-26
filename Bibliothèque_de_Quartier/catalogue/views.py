from django.db.models import Q
from django.views.generic import DetailView, ListView
from catalogue.models import Genre, Livre


class AccueilView(ListView):
    model = Livre
    template_name = "accueil.html"
    context_object_name = "livres"

    def get_queryset(self):
        return Livre.objects.select_related("genre").order_by("titre")[:4]


class ListeLivresView(ListView):
    model = Livre
    template_name = "catalogue/liste_livres.html"
    paginate_by = 24

    def get_queryset(self):
        queryset = Livre.objects.select_related("genre").order_by("titre")
        recherche = self.request.GET.get("recherche", "").strip()
        genre_selectionne = self.request.GET.get("genre", "")
        if recherche:
            filtres = Q(titre__icontains=recherche) | Q(auteur__icontains=recherche) | Q(genre__nom__icontains=recherche)
            if recherche.isdigit():
                filtres |= Q(annee=int(recherche))
            queryset = queryset.filter(filtres)
        if genre_selectionne.isdigit():
            queryset = queryset.filter(genre_id=int(genre_selectionne))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.order_by("nom")
        context["derniere_recherche"] = self.request.GET.get("recherche", "").strip()
        context["genre_selectionne"] = self.request.GET.get("genre", "")
        return context


class LivreDetailView(DetailView):
    model = Livre
    template_name = "catalogue/detail_livre.html"
    context_object_name = "livre"

    def get_queryset(self):
        return Livre.objects.select_related("genre")

    def get_context_data(self, **kwargs):
        from reservation.models import Reservation
        context = super().get_context_data(**kwargs)
        actifs = Reservation.objects.filter(livre=self.object, etat__in=Reservation.Etat).count()
        context["exemplaires_disponibles"] = max(self.object.exemplaires - actifs, 0)
        return context
