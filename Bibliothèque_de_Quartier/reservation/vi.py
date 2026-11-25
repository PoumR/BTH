from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from functools import wraps
from django.core.exceptions import PermissionDenied
from reservation.models import Reservation
from app.models.livre import Livre


@login_required
def liste_reservations(request):

    reservations = Reservation.objects.filter(
        emprunteur=request.user
    )

    return render(
        request,
        "reservation/liste_reservations.html",
        {"reservations": reservations}
    )


@login_required
def livres_a_reserver(request):

    livres = Livre.objects.all()

    return render(
        request,
        "reservation/livres_a_reserver.html",
        {"livres": livres}
    )


@login_required
def reserver_livre(request, livre_id):

    if request.method == "POST":

        livre = get_object_or_404(Livre, id=livre_id)

        reservation_existante = Reservation.objects.filter(
            emprunteur=request.user,
            livre=livre,
            etat__in=[
                Reservation.Etat.EN_ATTENTE,
                Reservation.Etat.ACCEPTEE,
            ]
        ).exists()

        if not reservation_existante:
            Reservation.objects.create(
                emprunteur=request.user,
                livre=livre,
                etat=Reservation.Etat.EN_ATTENTE
            )

    return redirect("reservation:livres_a_reserver")


@login_required
@require_POST
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        emprunteur=request.user,
        etat=Reservation.Etat.EN_ATTENTE,
    )
    reservation.etat = Reservation.Etat.ANNULEE
    reservation.save()

    return redirect("reservation:liste_reservations")


def gestionnaire_requis(vue):
    @login_required
    @wraps(vue)
    def _vue(request, *args, **kwargs):
        if request.user.role != request.user.Roles.GESTIONNAIRE:
            raise PermissionDenied
        return vue(request, *args, **kwargs)
    return _vue


#@gestionnaire_requis
def gestion_reservations(request):
    reservations = (
        Reservation.objects
        .select_related("livre", "emprunteur")
        .order_by("-date_creation")
    )
    return render(
        request,
        "reservation/gestion_reservations.html",
        {"reservations": reservations},
    )


#@gestionnaire_requis
@require_POST
def changer_etat_reservation(request, reservation_id):
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