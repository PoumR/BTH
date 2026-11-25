from django.test import TestCase
from django.urls import reverse
from app.models import Livre, Genre

class CatalogueTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        genre = Genre.objects.create(nom="Roman")
        cls.livre = Livre.objects.create(titre="Les Misérables", auteur="Victor Hugo", annee=1862, resume="Résumé", exemplaires=2, isbn="9780000000002", genre=genre)

    def test_catalogue_recherche(self):
        response = self.client.get(reverse("liste_livres"), {"recherche": "Hugo"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Les Misérables")

    def test_genre_filter(self):
        response = self.client.get(reverse("liste_livres"), {"genre": self.livre.genre_id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Les Misérables")

    def test_detail(self):
        self.assertEqual(self.client.get(reverse("detail_livre", args=[self.livre.pk])).status_code, 200)
