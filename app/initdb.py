import sqlite3
import os
from app.models.UserDAO import UserSqliteDAO

def init_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'database.db')
    schema_path = os.path.join(base_dir, 'schema.sql')
    print(f"Connexion à la base de données : {db_path}...")
    connection = sqlite3.connect(db_path)
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
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
            {"nom": "Antoine", "mdp": "anto123", "role": "Administrateur"},
            {"nom": "Sarah", "mdp": "sarah123", "role": ""},
            {"nom": "Janshica", "mdp": "janshica123", "role": ""},
            {"nom": "Floriane", "mdp": "floriane123", "role": ""},
            {"nom": "Nassim", "mdp": "nassim123", "role": ""}
        ]

        for u in utilisateurs:
            if not udao.findByUsername(u["nom"]):
                udao.createUser(u["nom"], u["mdp"], u["role"])
                print(f"   👤 Utilisateur '{u['nom']}' créé.")
        
        print("✅ Importation des utilisateurs terminée.")
    except Exception as e:
        print(f"❌ Erreur lors de l'import des utilisateurs : {e}")
if __name__ == '__main__':
    init_db()
