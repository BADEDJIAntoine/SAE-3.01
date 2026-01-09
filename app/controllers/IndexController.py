import sqlite3  # Import standard de Python (Ligne séparée)
from flask import render_template
from app import app
from app.controllers.LoginController import reqlogged, us

class IndexController:
    # ... le reste de ton code reste identique

    @app.route("/", methods=['GET'])
    @reqlogged
    def index():
        # On récupère les stats via notre UserService (qui a déjà le DAO)
        utilisateurs = us.getUsers()
        
        # Pour les autres stats, on ouvre une petite connexion rapide ici 
        # sans passer par un service externe
        db_path = app.root_path + '/database.db'
       # Récupération sécurisée
        utilisateurs = us.getUsers()
        nb_users = len(utilisateurs) if utilisateurs is not None else 0
        stats = {"nb_users": nb_users, "nb_lecteurs": 0, "nb_logs": 0} 
        
        try:
            conn = sqlite3.connect(db_path)
            stats["nb_lecteurs"] = conn.execute('SELECT COUNT(*) FROM Lecteur').fetchone()[0]
            stats["nb_logs"] = conn.execute('SELECT COUNT(*) FROM FichierLog').fetchone()[0]
            conn.close()
        except:
            pass # Si les tables n'existent pas encore, on affiche 0

        metadata = {"title": "Accueil Rythmo", "pagename": "index"}

        return render_template('index.html', metadata=metadata, stats=stats)