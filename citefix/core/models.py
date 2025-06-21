from mongoengine import *
from datetime import datetime

# === UTILISATEUR ===
class Utilisateur(Document):
    ROLES = ('citoyen', 'autorite_locale', 'technicien', 'admin', 'admin_sys')

    email = EmailField(required=True, unique=True)
    telephone = StringField(required=True, unique=True)
    mot_de_passe = StringField(required=True)  # À hasher avec bcrypt ou autre
    nom = StringField()
    prenom = StringField()
    photo_profil = StringField()  # URL ou nom de fichier
    bio = StringField()
    date_naissance = DateField()
    lieu_residence = StringField()
    role = StringField(choices=ROLES, required=True)
    est_actif = BooleanField(default=True)
    date_inscription = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"

# === CATEGORIE DE PLAINTE ===
class Categorie(Document):
    nom = StringField(required=True, unique=True)
    description = StringField()

    def __str__(self):
        return self.nom

# === PLAINTE ===
class Plainte(Document):
    STATUTS = (
        'Signalée', 'Validée', 'Rejetée', 'Affectée',
        'En intervention', 'Fin d’intervention', 'Réglée',
        'Résolue', 'Non résolue'
    )

    auteur = ReferenceField(Utilisateur, required=True)
    description = StringField(required=True)
    medias = ListField(StringField())  # URLs des photos/vidéos
    categorie = ReferenceField(Categorie, null=True)
    statut = StringField(choices=STATUTS, default='Signalée')
    localisation = StringField()
    date_creation = DateTimeField(default=datetime.utcnow)
    technicien_assigne = ReferenceField(Utilisateur, null=True)
    autorite_locale = ReferenceField(Utilisateur, null=True)

    def __str__(self):
        return f"Plainte #{str(self.id)[:6]} - {self.statut}"

# === COMMENTAIRE ===
class Commentaire(Document):
    plainte = ReferenceField(Plainte, required=True)
    auteur = ReferenceField(Utilisateur, required=True)
    texte = StringField(required=True)
    date_creation = DateTimeField(default=datetime.utcnow)
    signalement_raison = StringField(null=True)  # pour signalement éventuel

    def __str__(self):
        return f"Commentaire de {self.auteur.nom} sur plainte {str(self.plainte.id)[:6]}"

# === REACTION ===
class Reaction(Document):
    plainte = ReferenceField(Plainte, required=True)
    utilisateur = ReferenceField(Utilisateur, required=True)
    type_reaction = StringField(choices=['like', 'dislike'])  # like = plainte vraie, dislike = fausse
    date = DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': [
            {'fields': ('plainte', 'utilisateur'), 'unique': True}
        ]
    }

# === RECOMPENSE ===
class Recompense(Document):
    plainte = ReferenceField(Plainte, required=True)
    montant = FloatField()
    beneficiaire = ReferenceField(Utilisateur, required=True)
    role_benef = StringField(choices=['citoyen', 'technicien'])
    date_attribution = DateTimeField(default=datetime.utcnow)
