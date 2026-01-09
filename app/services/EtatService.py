def check_lecteurs_status(db):
    # Logique pour simuler ou vérifier si les lecteurs répondent
    # Retourne une liste mise à jour
    lecteurs = db.execute('SELECT * FROM lecteur').fetchall()
    # Ici on pourrait imaginer un ping réseau
    return lecteurs