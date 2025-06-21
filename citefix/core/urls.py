from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="accueil"),
    path('inscription', register_view, name="inscription"),
    path('connexion', login_view, name="connexion"),
    path('deconnexion', logout, name="deconnexion"),
    path('profil', profil, name="profil"),
]