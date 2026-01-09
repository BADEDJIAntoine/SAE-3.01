class User:
    def __init__(self, row):
        # row est un dictionnaire ou un sqlite3.Row
        self.id = row["id_utilisateur"]
        self.username = row["nom_utilisateur"]
        self.role = row["role"]



