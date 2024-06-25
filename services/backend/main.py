from datetime import datetime, timedelta
from flask_restx import Api
from flask import  jsonify, Flask
from app2.config import DevelopmentConfig

from flask.cli import FlaskGroup
from flask_cors import CORS

from parse_courses import *
from extensions import db
from models import *

import os
import time

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Inicializa la extensión de base de datos
db.init_app(app)

# Configuración de CORS
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:3000"],
    "methods": ["GET", "POST", "PATCH", "DELETE"],
    "allow_headers": ["Authorization", "Content-Type"],
    "supports_credentials": True,
    "max_age": 3600
}})


# Configuración de la API
api = Api(app, version="1.0", title="APIs", doc="/docs/")


################################### RUTAS AQUI ###################################



################################### FIN RUTAS ###################################





# Setup CORS
CORS(app)

# Create the database and tables if they don't exist
with app.app_context():
    time.sleep(10)  # Espera para asegurarse de que la base de datos esté lista
    db.create_all()
    print("se crearon modelos de la db")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')