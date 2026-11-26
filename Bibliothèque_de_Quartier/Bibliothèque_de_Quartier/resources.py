from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from users.models import Emprunteur
from reservation.models import Reservation
from catalogue.models.livre import Livre
from catalogue.models.genre import Genre

from django.conf import settings

class LivreResource(resources.ModelResource):
    genre = fields.Field(
        attribute='genre', 
        column_name='categorie_id',
        widget=ForeignKeyWidget(Genre, field='id') 
    )

    class Meta:
        model = Livre
        fields = ('id','titre','auteur','annee','genre','resume','exemplaires','isbn')

class ReservationResource(resources.ModelResource):
    emprunteur = fields.Field(
        attribute='emprunteur', 
        column_name='utilisateur_id',
        widget=ForeignKeyWidget(Emprunteur, field='id') 
    )
    livre = fields.Field(
        attribute='livre', 
        column_name='objet_id',
        widget=ForeignKeyWidget(Livre, field='id') 
    )

    class Meta:
        model = Reservation
        fields = ('id','emprunteur','livre','etat','date_creation','date_modification')

class EmprunteurResource(resources.ModelResource):

    class Meta:
        model = Emprunteur
        fields = ("id","prenom", "nom", "password", "email","role","numero_adherent")

    def before_save_instance(self, instance, row, **kwargs):
        # Ne hash que si c'est une création (pas une mise à jour)
        if not instance.pk:
            instance.set_password(settings.DEFAULT_PASSWORD)


CUSTOM_RESOURCES = {
    Livre: LivreResource,
    Reservation: ReservationResource,
    Emprunteur: EmprunteurResource,
}

def get_resource_for_model(model):
    resource_class = CUSTOM_RESOURCES.get(model)
    if resource_class:
        return resource_class()
    return resources.modelresource_factory(model=model)()
