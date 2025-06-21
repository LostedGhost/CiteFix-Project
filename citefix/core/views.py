from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur
import bcrypt
from .utils import save_file

def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.session.get("user_id", None):
        return redirect("profil")
    context = {}
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    context["error"] = error
    context["success"] = success
    context["roles"] = ('citoyen', 'technicien')
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        nom = request.POST.get('nom', None)
        prenom = request.POST.get('prenom', None)
        role = request.POST.get('role', None)
        #date_naissance = request.POST.get("date_naissance", None)
        telephone = request.POST.get('telephone', None)
        print(f"email = {email}")
        print(f"password = {password}")
        print(f"repassword = {repassword}")
        print(f"nom = {nom}")
        print(f"prenom = {prenom}")
        print(f"role = {role}")
        print(f"telephone = {telephone}")
        
        if not (email and password and repassword and nom and prenom and role and telephone):
            request.session["error"] = "Tous les champs sont à renseigner !!!"
            return redirect('inscription')
        
        if password != repassword:
            request.session["error"] = "Les mots de passe ne correspondent pas !!!"
            return redirect('inscription')

        if Utilisateur.objects(email=email).first():
            request.session["error"] = "Email déjà utilisé."
            return redirect('inscription')

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        Utilisateur(
            email=email,
            mot_de_passe=hashed_pw,
            nom=nom,
            prenom=prenom,
            role=role,
            telephone= telephone
        ).save()

        messages.success(request, "Compte créé avec succès. Connecte-toi maintenant.")
        return redirect('connexion')
    
    return render(request, 'auth/signin.html', context)


def login_view(request):
    if request.session.get("user_id", None):
        return redirect("profil")
    context = {}
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    context["error"] = error
    context["success"] = success
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = Utilisateur.objects(email=email).first()
        if not password:
            request.session["error"]  =  "Renseignez le mot de passe !!!"
            return redirect("connexion")
        if user and bcrypt.checkpw(password.encode(), user.mot_de_passe.encode()):
            request.session['user_id'] = str(user.id)
            return redirect('profil')
        request.session["error"]  =  "Identifiants incorrects."
        return redirect("connexion")
    return render(request, 'auth/login.html', context)

def logout(request):
    request.session.flush()
    return redirect("/")

def profil(request):
    if not request.session.get("user_id", None):
        return redirect("connexion")
    context = {}
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    context["error"] = error
    context["success"] = success
    user_id = request.session.get("user_id", None)
    user =  Utilisateur.objects(id=user_id).first()
    context["user"] = user
    if request.POST:
        if 'nom' in request.POST:
            photo = request.FILES.get("photo", None)
            nom = request.POST.get("nom", None)
            prenom = request.POST.get("prenom", None)
            bio = request.POST.get("bio", None)
            date_naissance = request.POST.get("date_naissance", None)
            if not (nom and prenom and bio, date_naissance):
                request.session['error'] = "Veuillez renseigner les champs avant modification !!!"
                return redirect("profil")
            if photo:
                nom_photo = save_file(photo, "profil_user")
                user.photo_profil = nom_photo
            user.nom = nom
            user.prenom = prenom
            user.bio = bio
            user.save()
            request.session['success'] = "Informations mises à jour avec succès !!!"
            return redirect("profil")
        elif 'oldPassword' in request.POST:
            oldPassword = request.POST.get('oldPassword', None)
            newPassword = request.POST.get('newPassword', None)
            rePassword = request.POST.get('rePassword', None)
            if not (user and bcrypt.checkpw(oldPassword.encode(), user.mot_de_passe.encode())):
                request.session['error'] = "Mot de passe incorrect !!!"
                return redirect("profil")
            if newPassword != rePassword:
                request.session['error'] = "Les mots de passes ne correspondent pas !!!"
                return redirect("profil")
            hashed_pw = bcrypt.hashpw(newPassword.encode(), bcrypt.gensalt()).decode()
            user.mot_de_passe = hashed_pw
            user.save()
            request.session['success'] = "Mot de passe modifié avec succès !!!"
            return redirect("profil")
    return render(request, "app/profil.html", context)
