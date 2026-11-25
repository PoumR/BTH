from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from app.models import Livre
from .models import Reservation


def est_gestionnaire(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or user.role == "gestionnaire")

class GestionnaireRequisMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return est_gestionnaire(self.request.user)

class ListeReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/liste_reservations.html"
    context_object_name = "reservations"
    def get_queryset(self):
        return Reservation.objects.filter(emprunteur=self.request.user).select_related("livre").order_by("-date_creation")

class LivresAReserverView(LoginRequiredMixin, ListView):
    model = Livre
    template_name = "reservation/livres_a_reserver.html"
    context_object_name = "livres"
    def get_queryset(self):
        return Livre.objects.order_by("titre")

class ReserverLivreView(LoginRequiredMixin, View):
    http_method_names = ["post"]
    def post(self, request, livre_id=None, pk=None):
        livre_id = livre_id or pk
        with transaction.atomic():
            livre = get_object_or_404(Livre.objects.select_for_update(), pk=livre_id)
            if est_gestionnaire(request.user):
                messages.error(request, "Les réservations sont destinées aux adhérents.")
            elif Reservation.objects.filter(emprunteur=request.user, etat__in=Reservation.ETATS_ACTIFS).count() >= 3:
                messages.error(request, "Vous avez déjà trois réservations actives.")
            elif Reservation.objects.filter(emprunteur=request.user, livre=livre, etat__in=Reservation.ETATS_ACTIFS).exists():
                messages.error(request, "Vous avez déjà réservé ce titre.")
            elif Reservation.objects.filter(livre=livre, etat__in=Reservation.ETATS_ACTIFS).count() >= livre.exemplaires:
                messages.error(request, "Tous les exemplaires sont déjà réservés.")
            else:
                Reservation.objects.create(emprunteur=request.user, livre=livre)
                messages.success(request, "Votre demande de réservation est enregistrée.")
        return redirect("reservation:liste_reservations")

class AnnulerReservationView(LoginRequiredMixin, View):
    http_method_names = ["post"]
    def post(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, pk=reservation_id, emprunteur=request.user)
        try:
            reservation.changer_etat(Reservation.Etat.ANNULEE)
        except ValueError:
            messages.error(request, "Cette réservation ne peut plus être annulée.")
        else:
            messages.success(request, "Réservation annulée.")
        return redirect("reservation:liste_reservations")

class GestionReservationsView(GestionnaireRequisMixin, ListView):
    model = Reservation
    template_name = "reservation/gestion_reservations.html"
    context_object_name = "reservations"
    def get_queryset(self):
        return Reservation.objects.select_related("livre", "emprunteur").order_by("-date_creation")

class ChangerEtatReservationView(GestionnaireRequisMixin, View):
    http_method_names = ["post"]
    def post(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        try:
            reservation.changer_etat(request.POST.get("etat"), gestionnaire=True)
        except ValueError:
            messages.error(request, "Transition d'état non autorisée.")
        else:
            messages.success(request, "État de la réservation mis à jour.")
        return redirect("reservation:gestion")
