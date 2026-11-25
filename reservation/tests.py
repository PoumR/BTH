from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from app.models import Genre, Livre
from .models import Reservation

class ReservationsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(nom="Roman")
        cls.livre = Livre.objects.create(titre="Test", auteur="Autrice", annee=2020, resume="Résumé", exemplaires=1, isbn="9780000000001", genre=cls.genre)
        User = get_user_model()
        cls.adherent = User.objects.create_user(email="adherent@test.fr", password="secret-12345", role="adhérent", numero_adherent="BIB-9991", nom="Test", prenom="Alice")
        cls.gestionnaire = User.objects.create_user(email="gestion@test.fr", password="secret-12345", role="gestionnaire", numero_adherent="BIB-9992", nom="Test", prenom="Bob")

    def test_reservation_login_required(self):
        response = self.client.post(reverse("reservation:reserver_livre", args=[self.livre.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_reservation_capacity(self):
        self.client.force_login(self.adherent)
        url = reverse("reservation:reserver_livre", args=[self.livre.pk])
        self.client.post(url)
        self.client.post(url)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_only_manager_can_manage(self):
        url = reverse("reservation:gestion")
        self.client.force_login(self.adherent)
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.force_login(self.gestionnaire)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_cancel_allowed(self):
        r = Reservation.objects.create(emprunteur=self.adherent, livre=self.livre)
        self.client.force_login(self.adherent)
        self.client.post(reverse("reservation:annuler_reservation", args=[r.pk]))
        r.refresh_from_db()
        self.assertEqual(r.etat, Reservation.Etat.ANNULEE)
