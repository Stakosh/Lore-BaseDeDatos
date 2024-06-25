from datetime import datetime, timedelta
from flask_restx import Api, Resource, Namespace, fields
from sqlalchemy import Enum 
from flask import jsonify, Flask, request
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

# Namespace para operaciones relacionadas con estadísticas de escuelas
stats_ns = Namespace('stats', description='Estadísticas de escuelas')

# Modelo para creación y actualización de escuelas
school_model = stats_ns.model('School', {
    'ID_Escuela': fields.Integer(description='ID de la escuela'),
    'Nombre': fields.String(required=True, description='Nombre de la escuela'),
    'ID_Comuna': fields.Integer(required=True, description='ID de la comuna'),
    'Infraestructura': fields.String(required=True, description='Estado de la infraestructura'),
    'Acceso_Educacion': fields.Integer(description='Acceso a la educación'),
    'Finalizacion_Basica': fields.Integer(description='Finalización de educación básica'),
    'Finalizacion_Media': fields.Integer(description='Finalización de educación media'),
    'Mujeres_Acceso': fields.Integer(description='Acceso a la educación para mujeres'),
    'Mujeres_Finalizacion': fields.Integer(description='Finalización de educación para mujeres'),
    'Acceso_Superior': fields.Integer(description='Acceso a educación superior'),
    'Preparacion_Maestros': fields.String(required=True, description='Nivel de preparación de los maestros')
})

# Modelo para Comuna
comuna_model = stats_ns.model('Comuna', {
    'ID_Comuna': fields.Integer(description='ID de la comuna'),
    'Nombre': fields.String(required=True, description='Nombre de la comuna'),
    'ID_Region': fields.Integer(required=True, description='ID de la región')
})

# Modelo para Región
region_model = stats_ns.model('Region', {
    'ID_Region': fields.Integer(description='ID de la región'),
    'Nombre': fields.String(required=True, description='Nombre de la región')
})

# Modelo para Conflicto
conflicto_model = stats_ns.model('Conflicto', {
    'ID_Conflicto': fields.Integer(description='ID del conflicto'),
    'Tipo': fields.String(required=True, description='Tipo de conflicto'),
    'ID_Comuna': fields.Integer(required=True, description='ID de la comuna')
})

# Modelo para Catástrofe
catastrofe_model = stats_ns.model('Catastrofe', {
    'ID_Catastrofe': fields.Integer(description='ID de la catástrofe'),
    'Tipo': fields.String(required=True, description='Tipo de catástrofe'),
    'Frecuencia': fields.Integer(description='Frecuencia de la catástrofe'),
    'ID_Comuna': fields.Integer(required=True, description='ID de la comuna')
})

################################### RUTAS AQUI ###################################


def to_dict_with_enum(obj):
    """Convert an SQLAlchemy object to a dictionary, incluyendo valores Enum como cadenas."""
    if not obj:
        return None
    result = {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
    for key, value in result.items():
        if isinstance(value, enum.Enum):
            result[key] = value.name  # Convierte Enum a su nombre
    return result


# Rutas para las estadísticas
@app.route('/api/stats/total_schools', methods=['GET'])
def total_schools():
    total = db.session.query(Escuela).count()
    return jsonify(total_schools=total)

@app.route('/api/stats/schools_by_comuna', methods=['GET'])
def schools_by_comuna():
    schools_by_comuna = db.session.query(Comuna.Nombre, db.func.count(Escuela.ID_Escuela)).join(Escuela).group_by(Comuna.Nombre).all()
    result = {comuna: count for comuna, count in schools_by_comuna}
    return jsonify(schools_by_comuna=result)

@app.route('/api/stats/good_infrastructure_percentage', methods=['GET'])
def good_infrastructure_percentage():
    total_schools = db.session.query(Escuela).count()
    good_infrastructure = db.session.query(Escuela).filter(Escuela.Infraestructura == InfraestructuraEnum.Buena).count()
    percentage = (good_infrastructure / total_schools) * 100 if total_schools > 0 else 0
    return jsonify(good_infrastructure_percentage=percentage)

@app.route('/api/stats/completion_rates', methods=['GET'])
def completion_rates():
    avg_completion_basic = db.session.query(db.func.avg(Escuela.Finalizacion_Basica)).scalar()
    avg_completion_media = db.session.query(db.func.avg(Escuela.Finalizacion_Media)).scalar()
    return jsonify(average_completion_basic=avg_completion_basic, average_completion_media=avg_completion_media)

@app.route('/api/stats/worst_schools/<string:comuna_name>', methods=['GET'])
def worst_schools(comuna_name):
    worst_schools = db.session.query(Escuela).join(Comuna).filter(
        Comuna.Nombre == comuna_name,
        db.or_(Escuela.Infraestructura == InfraestructuraEnum.Mala, Escuela.Preparacion_Maestros == PreparacionMaestrosEnum.Bajo)
    ).all()

    result = [
        to_dict_with_enum(escuela)
        for escuela in worst_schools
    ]
    
    return jsonify(worst_schools=result)

@app.route('/api/stats/schools/filter', methods=['GET'])
def filter_schools():
    comuna_name = request.args.get('comuna')

    query = db.session.query(Escuela).join(Comuna)

    if comuna_name:
        query = query.filter(Comuna.Nombre == comuna_name)

    result = query.all()

    schools = [
        to_dict_with_enum(school)
        for school in result
    ]

    return jsonify(schools=schools)

# Rutas para los colegios vulnerables y mejores colegios
@app.route('/api/vulnerable-schools', methods=['GET'])
def vulnerable_schools():
    schools = db.session.query(Escuela).order_by(Escuela.Acceso_Educacion).limit(10).all()
    return jsonify([to_dict_with_enum(school) for school in schools])

@app.route('/api/top-schools', methods=['GET'])
def top_schools():
    schools = db.session.query(Escuela).order_by(Escuela.Acceso_Superior.desc()).limit(10).all()
    return jsonify([to_dict_with_enum(school) for school in schools])

@app.route('/api/stats/all_comunas', methods=['GET'])
def all_comunas():
    comunas = db.session.query(Comuna.Nombre).all()
    comunas_list = [comuna.Nombre for comuna in comunas]
    return jsonify(comunas=comunas_list)

################################### FIN RUTAS ###################################




# Create the database and tables if they don't exist
with app.app_context():
    time.sleep(2)  # Espera para asegurarse de que la base de datos esté lista
    db.create_all()
    print("se crearon modelos de la db")
    read_csv_and_insert_data("/app/data/base_de_datos_chile.csv")
    print("datos insertados correctamente")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
