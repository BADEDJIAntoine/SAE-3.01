import sqlite3
import os
from app.models.UserDAO import UserSqliteDAO
def init_db():
    # 1. Définition des chemins (on se base sur l'emplacement de ce fichier)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'database.db')
    schema_path = os.path.join(base_dir, 'schema.sql')

    # 2. Connexion à la base de données
    print(f"Connexion à la base de données : {db_path}...")
    connection = sqlite3.connect(db_path)

    # 3. Lecture et exécution du fichier schema.sql
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        # executeScript permet de lancer plusieurs commandes SQL d'un coup
        connection.executescript(sql_script)
        connection.commit()
        print("✅ Succès : Les tables ont été créées et initialisées.")
        
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{schema_path}' est introuvable.")
    except sqlite3.Error as e:
        print(f"❌ Erreur SQLite : {e}")
    finally:
        connection.close()

    print("Insertion des utilisateurs de test...")
    try:
        udao = UserSqliteDAO()
        utilisateurs = [
            {"nom": "admin_principal", "mdp": "admin123", "role": "Administrateur"},
            {"nom": "jean_dupont", "mdp": "jean789", "role": "Superviseur"},
            {"nom": "marie_lefebvre", "mdp": "marie456", "role": "Opérateur"}
        ]

        for u in utilisateurs:
            # On vérifie si l'utilisateur existe déjà pour éviter les erreurs au redémarrage
            if not udao.findByUsername(u["nom"]):
                # On utilise TA méthode createUser pour hacher le mot de passe
                udao.createUser(u["nom"], u["mdp"], u["role"])
                print(f"   👤 Utilisateur '{u['nom']}' créé.")
        
        print("✅ Importation des utilisateurs terminée.")
    except Exception as e:
        print(f"❌ Erreur lors de l'import des utilisateurs : {e}")
if __name__ == '__main__':
    init_db()
