from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from app.models.reservation import Reservation
from .models.emprunteur import Emprunteur
from .models.livre import Livre
from .models.genre import Genre

class LivreResource(resources.ModelResource):
    # Mapping uniquement pour 'prenom' qui s'appelle 'First_Name' dans le CSV
    genre = fields.Field(
        attribute='genre', 
        column_name='categorie_id',
        widget=ForeignKeyWidget(Genre, field='id') 
    )

    class Meta:
        model = Livre
        fields = ('id','titre','auteur','annee','genre','resume','exemplaires','isbn')

class ReservationResource(resources.ModelResource):
    # Mapping uniquement pour 'prenom' qui s'appelle 'First_Name' dans le CSV
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


CUSTOM_RESOURCES = {
    Livre: LivreResource,
    Reservation: ReservationResource,
}

def get_resource_for_model(model):
    resource_class = CUSTOM_RESOURCES.get(model)
    if resource_class:
        return resource_class()
    return resources.modelresource_factory(model=model)()