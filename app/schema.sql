-- Création de la table des lecteurs
DROP TABLE IF EXISTS Utilisateur;
CREATE TABLE Utilisateur(
   id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
   nom_utilisateur VARCHAR(50),
   motdepasse VARCHAR(50),
   role VARCHAR(50),
   UNIQUE(nom_utilisateur)
);

CREATE TABLE Playlist(
   id_playlist INT,
   nom_playlist VARCHAR(50),
   date_creation DATE,
   date_fin_playlist DATE,
   date_derniere_maj DATE,
   PRIMARY KEY(id_playlist),
   UNIQUE(nom_playlist)
);

CREATE TABLE Planification(
   planning_jour DATE,
   PRIMARY KEY(planning_jour)
);

CREATE TABLE Organisation(
   id_organisation INT,
   nom_organisation VARCHAR(50),
   PRIMARY KEY(id_organisation),
   UNIQUE(nom_organisation)
);

CREATE TABLE Fichier(
   id_fichier INT,
   nom VARCHAR(50),
   emplacement VARCHAR(50),
   duree_fichier INT,
   date_maj DATE,
   PRIMARY KEY(id_fichier),
   UNIQUE(nom)
);

CREATE TABLE Type(
   id_type INT,
   nom_type VARCHAR(50),
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_type),
   FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id_utilisateur)
);

DROP TABLE IF EXISTS FichierLog;

CREATE TABLE FichierLog (
    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
    type_fichierlog VARCHAR(50), -- ex: 'info', 'warning', 'error'
    message VARCHAR(255),
    date_fichierlog DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO FichierLog (type_fichierlog, message) VALUES ('info', 'Démarrage du système réussi');
INSERT INTO FichierLog (type_fichierlog, message) VALUES ('warning', 'Tentative de connexion suspecte');

CREATE TABLE Lecteur(
   id_lecteur INT,
   nom_lecteur VARCHAR(50) NOT NULL,
   adresseIP VARCHAR(50),
   etat_lecteur VARCHAR(50),
   emplacement VARCHAR(50),
   derniere_synchro DATE,
   adresse_lecteur VARCHAR(50),
   id_organisation INT NOT NULL,
   PRIMARY KEY(id_lecteur),
   UNIQUE(nom_lecteur),
   UNIQUE(adresseIP),
   FOREIGN KEY(id_organisation) REFERENCES Organisation(id_organisation)
);

CREATE TABLE Conçoit_une(
   id_utilisateur INT,
   id_playlist INT,
   PRIMARY KEY(id_utilisateur, id_playlist),
   FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
   FOREIGN KEY(id_playlist) REFERENCES Playlist(id_playlist)
);

CREATE TABLE Est_composé_d_une(
   id_playlist INT,
   id_fichier INT,
   PRIMARY KEY(id_playlist, id_fichier),
   FOREIGN KEY(id_playlist) REFERENCES Playlist(id_playlist),
   FOREIGN KEY(id_fichier) REFERENCES Fichier(id_fichier)
);

CREATE TABLE planifie_une(
   id_playlist INT,
   planning_jour DATE,
   PRIMARY KEY(id_playlist, planning_jour),
   FOREIGN KEY(id_playlist) REFERENCES Playlist(id_playlist),
   FOREIGN KEY(planning_jour) REFERENCES Planification(planning_jour)
);

CREATE TABLE Travaille_ensemble(
   id_utilisateur INT,
   id_organisation INT,
   PRIMARY KEY(id_utilisateur, id_organisation),
   FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
   FOREIGN KEY(id_organisation) REFERENCES Organisation(id_organisation)
);

DROP TABLE IF EXISTS etudiant;
