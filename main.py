from app import app
import sqlite3
import os

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
