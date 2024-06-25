import csv
import bcrypt
from extensions import db
from models import *
import csv
from flask_sqlalchemy import SQLAlchemy

def create_tables():
    db.create_all()

def read_csv_and_insert_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Tabla'] == 'Region':
                insert_region(row)
            elif row['Tabla'] == 'Comuna':
                insert_comuna(row)
            elif row['Tabla'] == 'Escuela':
                insert_escuela(row)
            elif row['Tabla'] == 'Conflicto':
                insert_conflicto(row)
            elif row['Tabla'] == 'Catastrofe':
                insert_catastrofe(row)
        db.session.commit()

def insert_region(row):
    region = Region(ID_Region=row['ID'], Nombre=row['Nombre'])
    db.session.add(region)

def insert_comuna(row):
    comuna = Comuna(ID_Comuna=row['ID'], Nombre=row['Nombre'], ID_Region=row['ID_Region'])
    db.session.add(comuna)

def insert_escuela(row):
    escuela = Escuela(
        ID_Escuela=row['ID'],
        Nombre=row['Nombre'],
        ID_Comuna=row['ID_Comuna'],
        Infraestructura=row['Infraestructura'],
        Acceso_Educacion=row['Acceso_Educacion'],
        Finalizacion_Basica=row['Finalizacion_Basica'],
        Finalizacion_Media=row['Finalizacion_Media'],
        Mujeres_Acceso=row['Mujeres_Acceso'],
        Mujeres_Finalizacion=row['Mujeres_Finalizacion'],
        Acceso_Superior=row['Acceso_Superior'],
        Preparacion_Maestros=row['Preparacion_Maestros']
    )
    db.session.add(escuela)

def insert_conflicto(row):
    conflicto = Conflicto(
        ID_Conflicto=row['ID'],
        Tipo=row['Tipo'],
        ID_Comuna=row['ID_Comuna']
    )
    db.session.add(conflicto)

def insert_catastrofe(row):
    catastrofe = Catastrofe(
        ID_Catastrofe=row['ID'],
        Tipo=row['Tipo'],
        Frecuencia=row['Frecuencia'],
        ID_Comuna=row['ID_Comuna']
    )
    db.session.add(catastrofe)
