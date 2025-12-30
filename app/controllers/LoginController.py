from flask import render_template, redirect, url_for, request
# imports nécessaires pour la connexion
from flask import session, flash
from flask import  abort
from app import app
from functools import wraps

from app.services.UserService import UserService

def reqlogged(f):
	@wraps(f) # permet de conserver le nom de la fonction, la nouvelle doc et les arguments
	def wrap(*args, **kwargs):
		if 'logged' in session:
			return f(*args, **kwargs)
		else:
			flash('Denied. You need to login.') # message flash
			return redirect(url_for('login'))
	return wrap


def reqrole(role):
	"""
	Décorateur vérifiant si l'utilisateur est connecté et s'il a le rôle requis.
	On peut y ajouter la hiérarchisation des rôles en intégrant une meilleure séparation des types d'action possible dans la BDD (et donc une table role)
	"""
	def wrap(f):
		@wraps(f) # permet de conserver le nom de la fonction, la nouvelle doc et les arguments
		def verifyRole(*args, **kwargs):
			# vérifie si l'utilisateur est connecté
			if not session.get('logged'):
				# s'il n'est pas connecté, retour à la page de login
				return redirect(url_for('login'))

			# vérifie le rôle
			current_role = session.get('role')
			if current_role != role:
				# Logged in but insufficient role, return a 403 Forbidden error
				# s'il est connecté mais que le rôle ne permet pas l'accès, retourne 403 forbidden error
				abort(403)

			# Si tout est ok, retourne la fonction
			return f(*args, **kwargs)
		return verifyRole
	return wrap


us = UserService()

class LoginController:

	@app.route('/login', methods=['GET', 'POST'])
	def login():
		msg_error = None
		if request.method == 'POST':
			user = us.login(request.form["username"], request.form["password"])
			if user:
				# on indique qu'il est connecté
				session["logged"] = True
				# on enregistre le nom de l'utilisateur dans la session, ainsi on peut y accéder dans le template
				session["username"] = user.username
				# on indique le role récupéré de la BDD
				session["role"] = user.role
				return redirect(url_for("index"))
			else:
				msg_error = 'Invalid Credentials'
		return render_template('login.html', msg_error=msg_error)
	
	@app.route("/signin", methods=['GET', 'POST'])
	def signin():
		if request.method == "POST":
			result = us.signin(request.form["username"], request.form["password"])
			if result:
				session["logged"] = True
				session["username"] = request.form["username"]
				session["role"] = "lecteur"
				return redirect(url_for('index'))
			else:
				return render_template("signin.html", msg_error="creation error")
		else:
			return render_template('signin.html', msg_error=None)


	@app.route('/logout')
	@reqlogged
	def logout():
		session.clear()
		flash('Successfully logged out')
		return redirect(url_for('login'))


