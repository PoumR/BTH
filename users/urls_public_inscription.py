from django.urls import path
from .views import CreateInscriptionView
urlpatterns = [path("", CreateInscriptionView.as_view(), name="inscription_public")]
