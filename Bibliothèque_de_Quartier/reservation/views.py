from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from app.models.livre import Livre
from reservation.models import Reservation


# ---------- Mixin réutilisable pour le gestionnaire ----------

class GestionnaireRequisMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Remplace le décorateur @gestionnaire_requis."""

    def test_func(self):
        user = self.request.user
        return user.role #== user.Roles.GESTIONNAIRE


# ---------- Côté emprunteur ----------

class ListeReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/liste_reservations.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return Reservation.objects.filter(emprunteur=self.request.user)


class LivresAReserverView(LoginRequiredMixin, ListView):
    model = Livre
    template_name = "reservation/livres_a_reserver.html"
    context_object_name = "livres"


class ReserverLivreView(LoginRequiredMixin, View):
    http_method_names = ["post"]  # GET -> 405, comme ton "if request.method == POST"

    def post(self, request, livre_id):
        livre = get_object_or_404(Livre, id=livre_id)

        reservation_existante = Reservation.objects.filter(
            emprunteur=request.user,
            livre=livre,
            etat__in=[
                Reservation.Etat.EN_ATTENTE,
                Reservation.Etat.ACCEPTEE,
            ],
        ).exists()

        if not reservation_existante:
            Reservation.objects.create(
                emprunteur=request.user,
                livre=livre,
                etat=Reservation.Etat.EN_ATTENTE,
            )

        return redirect("reservation:livres_a_reserver")


class AnnulerReservationView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, reservation_id):
        reservation = get_object_or_404(
            Reservation,
            id=reservation_id,
            emprunteur=request.user,
            etat=Reservation.Etat.EN_ATTENTE,
        )
        reservation.etat = Reservation.Etat.ANNULEE
        reservation.save()

        return redirect("reservation:liste_reservations")


# ---------- Côté gestionnaire ----------

class GestionReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/gestion_reservations.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return (
            Reservation.objects
            .select_related("livre", "emprunteur")
            .order_by("-date_creation")
        )


class ChangerEtatReservationView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        try:
            reservation.changer_etat(request.POST.get("etat"), gestionnaire=True)
        except ValueError:
            messages.error(request, "Ce changement d'état n'est pas autorisé.")
        else:
            messages.success(
                request,
                f"Réservation passée à l'état « {reservation.get_etat_display()} ».",
            )
        return redirect("reservation:gestion")