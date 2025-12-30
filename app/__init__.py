from flask import Flask

app = Flask(__name__, static_url_path='/static')
# on indique qu'on veut utiliser les cookies securisés pour éviter toute diffusion de nos informations
app.config["SESSION_COOKIE_SECURE"] = True
# la configuration de la clé secrète est obligatoire
app.secret_key = 'ma cle secrete unique'

from app.controllers import *


## filtre Jinja très simple
def toFrench(name):
	if name.lower() == "squirtle":
		return "carapuce"
	return name

app.jinja_env.filters['french'] = toFrench