from flask import Flask

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_COOKIE_SECURE"] = True
# la configuration de la clé secrète est obligatoire
app.secret_key = 'ma cle secrete unique'

from app.controllers import *

def toFrench(name):
	if name.lower() == "squirtle":
		return "carapuce"
	return name

app.jinja_env.filters['french'] = toFrench

