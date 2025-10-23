from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "clave_super_segura"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://SOFTWARE1:kevin190305@kevin\\SQLEXPRESS/ALITAS EL COMELON SF?driver=ODBC+Driver+17+for+SQL+Server'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models.login_crear_usuario import *

if __name__ == '__main__':
    app.run(debug=True)
