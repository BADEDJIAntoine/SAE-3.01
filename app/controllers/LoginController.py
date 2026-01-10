from flask import render_template, redirect, url_for, request, session, flash, abort
from app import app
from functools import wraps
from app.services.UserService import UserService
from app.services.LogService import add_log

us = UserService()

def reqlogged(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged' in session:
            return f(*args, **kwargs)
        else:
            flash('Accès refusé. Veuillez vous connecter.')
            return redirect(url_for('login'))
    return wrap

def reqrole(role):
    def wrap(f):
        @wraps(f)
        def verifyRole(*args, **kwargs):
            if not session.get('logged'):
                return redirect(url_for('login'))
            if session.get('role') != role:
                abort(403)
            return f(*args, **kwargs)
        return verifyRole
    return wrap

class LoginController:

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        msg_error = None
        if request.method == 'POST':
            username = request.form.get("nom_utilisateur")
            password = request.form.get("motdepasse")
            
            user = us.login(username, password)
            
            if user:
                session["logged"] = True
                session["nom_utilisateur"] = user.username
                session["role"] = user.role
                add_log('Connexion', f"L'utilisateur {user.username} s'est connecté.")
                return redirect(url_for("index"))
            else:
                msg_error = 'Identifiants invalides'
        return render_template('login.html', msg_error=msg_error)
    
    @app.route("/signin", methods=['GET', 'POST'])
    def signin():
        msg_error = None
        if request.method == "POST":
            username = request.form.get("nom_utilisateur")
            password = request.form.get("motdepasse")
            
            result = us.signin(username, password)
            if result:
                session["logged"] = True
                session["nom_utilisateur"] = username
                session["role"] = "lecteur"
                add_log('Création', f"Nouveau compte créé : {username}")
                return redirect(url_for('index'))
            else:
                msg_error = "Erreur lors de la création du compte"
        
        return render_template('signin.html', msg_error=msg_error)

    @app.route('/logout')
    def logout():
        user = session.get("nom_utilisateur")
        add_log('Déconnexion', f"L'utilisateur {user} s'est déconnecté.")
        session.clear()
        return redirect(url_for('login'))

