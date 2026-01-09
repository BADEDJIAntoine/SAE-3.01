import os
import bcrypt
import sqlite3
from app import app
from app.models.User import User
from app.models.UserDAOInterface import UserDAOInterface

class UserSqliteDAO(UserDAOInterface):
    def __init__(self):
        # Utilisation de database.db pour correspondre à ton initdb.py
        self.databasename = os.path.join(app.root_path, 'database.db')
        self._initTable()

    def _getDbConnection(self):
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def _initTable(self):
        conn = self._getDbConnection()
        # Note : On utilise INTEGER PRIMARY KEY AUTOINCREMENT pour simplifier
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Utilisateur(
               id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
               nom_utilisateur VARCHAR(50),
               motdepasse VARCHAR(50),
               role VARCHAR(50),
               UNIQUE(nom_utilisateur)
            )
        ''')
        conn.commit()
        conn.close()

    def _generatePwdHash(self, password):
        password_bytes = password.encode('utf-8')
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode('utf-8')

    def createUser(self, username, password, role='lecteur'):
        conn = self._getDbConnection()
        hashed_password = self._generatePwdHash(password)
        try:
            # CORRECTION : Les clés du dictionnaire DOIVENT correspondre aux :marqueurs
            conn.execute(
                "INSERT INTO Utilisateur (nom_utilisateur, motdepasse, role) VALUES (:u, :p, :r)",
                {
                    "u": username, 
                    "p": hashed_password, 
                    "r": role
                }
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def findByUsername(self, username):
        conn = self._getDbConnection()
        # Correction ici aussi pour le dictionnaire de paramètres
        user = conn.execute(
            "SELECT * FROM Utilisateur WHERE nom_utilisateur = :u", 
            {"u": username}
        ).fetchone()
        conn.close()
        return User(user) if user else None

    def verifyUser(self, username, password):
        conn = self._getDbConnection()
        user = conn.execute(
            "SELECT * FROM Utilisateur WHERE nom_utilisateur = :u", 
            {"u": username}
        ).fetchone()
        conn.close()
        
        if user:
            password_bytes = password.encode('utf-8')
            # ATTENTION : vérifie si ta colonne s'appelle 'motdepasse' ou 'password'
            stored_hash = user['motdepasse'].encode('utf-8')
            
            if bcrypt.checkpw(password_bytes, stored_hash):
                return User(user)
        return None
def findAll(self):
		""" trouve tous les users """
		conn = self._getDbConnection()
		users = conn.execute('SELECT * FROM Utilisateur').fetchall()
		instances = list()
		for user in users:
			instances.append(User(dict(user)))
		conn.close()
		return instances