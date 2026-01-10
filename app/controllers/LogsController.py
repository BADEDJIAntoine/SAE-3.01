import sqlite3
import os
from flask import render_template
from app import app
from app.controllers.LoginController import reqlogged

class LogController:

    @app.route("/logs", methods=['GET'])
    @reqlogged
    def logs():
        db_path = os.path.join(app.root_path, 'database.db')
        logs_data = []

        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            logs_data = conn.execute('SELECT * FROM FichierLog ORDER BY date_fichierlog DESC').fetchall()
            conn.close()
        except sqlite3.OperationalError:
            pass

        metadata = {"title": "Journal des Logs", "pagename": "logs"}
        return render_template('logs.html', metadata=metadata, logs=logs_data)