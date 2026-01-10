import sqlite3
from datetime import datetime
from app import app

def add_log(log_type, message):
    """ Enregistre une action dans la table FichierLog """
    try:
        db_path = app.root_path + '/database.db'
        conn = sqlite3.connect(db_path)
        conn.execute('''
            INSERT INTO FichierLog (type_fichierlog, message) 
            VALUES (?, ?)
        ''', (log_type, message))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'écriture du log : {e}")