import csv
import logging
from extensions import db
from models import *

# Configuración del registro
logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s %(message)s')

def read_csv_and_insert_data(file_path):
    print("Iniciando la lectura del archivo CSV...")
    logging.info("Iniciando la lectura del archivo CSV...")
    
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        regions = []
        comunas = []
        escuelas = []
        conflictos = []
        catastrofes = []
        
        for row in reader:
            if row['Tabla'] == 'Region':
                regions.append(row)
            elif row['Tabla'] == 'Comuna':
                comunas.append(row)
            elif row['Tabla'] == 'Escuela':
                escuelas.append(row)
            elif row['Tabla'] == 'Conflicto':
                conflictos.append(row)
            elif row['Tabla'] == 'Catastrofe':
                catastrofes.append(row)
        
        print(f"Total de regiones a insertar: {len(regions)}")
        logging.info(f"Total de regiones a insertar: {len(regions)}")
        insert_regions(regions)
        
        print(f"Total de comunas a insertar: {len(comunas)}")
        logging.info(f"Total de comunas a insertar: {len(comunas)}")
        insert_comunas(comunas)
        
        print(f"Total de escuelas a insertar: {len(escuelas)}")
        logging.info(f"Total de escuelas a insertar: {len(escuelas)}")
        insert_escuelas(escuelas)
        
        print(f"Total de conflictos a insertar: {len(conflictos)}")
        logging.info(f"Total de conflictos a insertar: {len(conflictos)}")
        insert_conflictos(conflictos)
        
        print(f"Total de catástrofes a insertar: {len(catastrofes)}")
        logging.info(f"Total de catástrofes a insertar: {len(catastrofes)}")
        insert_catastrofes(catastrofes)
        
        print("Todos los datos han sido insertados correctamente.")
        logging.info("Todos los datos han sido insertados correctamente.")

def insert_regions(regions):
    print("Iniciando la inserción de regiones...")
    logging.info("Iniciando la inserción de regiones...")
    
    existing_ids = {str(r.ID_Region) for r in db.session.query(Region.ID_Region).all()}
    new_regions = [Region(ID_Region=row['ID'], Nombre=row['Nombre']) for row in regions if row['ID'] not in existing_ids]
    
    if new_regions:
        db.session.bulk_save_objects(new_regions)
        db.session.commit()
        print("Regiones insertadas correctamente.")
        logging.info("Regiones insertadas correctamente.")
    else:
        print("No hay nuevas regiones para insertar.")
        logging.info("No hay nuevas regiones para insertar.")

def insert_comunas(comunas):
    print("Iniciando la inserción de comunas...")
    logging.info("Iniciando la inserción de comunas...")
    
    existing_ids = {str(c.ID_Comuna) for c in db.session.query(Comuna.ID_Comuna).all()}
    new_comunas = [Comuna(ID_Comuna=row['ID'], Nombre=row['Nombre'], ID_Region=row['ID_Region']) for row in comunas if row['ID'] not in existing_ids]
    
    if new_comunas:
        db.session.bulk_save_objects(new_comunas)
        db.session.commit()
        print("Comunas insertadas correctamente.")
        logging.info("Comunas insertadas correctamente.")
    else:
        print("No hay nuevas comunas para insertar.")
        logging.info("No hay nuevas comunas para insertar.")

def insert_escuelas(escuelas):
    print("Iniciando la inserción de escuelas...")
    logging.info("Iniciando la inserción de escuelas...")
    
    existing_ids = {str(e.ID_Escuela) for e in db.session.query(Escuela.ID_Escuela).all()}
    new_escuelas = [
        Escuela(
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
        ) for row in escuelas if row['ID'] not in existing_ids
    ]
    
    if new_escuelas:
        db.session.bulk_save_objects(new_escuelas)
        db.session.commit()
        print("Escuelas insertadas correctamente.")
        logging.info("Escuelas insertadas correctamente.")
    else:
        print("No hay nuevas escuelas para insertar.")
        logging.info("No hay nuevas escuelas para insertar.")

def insert_conflictos(conflictos):
    print("Iniciando la inserción de conflictos...")
    logging.info("Iniciando la inserción de conflictos...")
    
    existing_ids = {str(c.ID_Conflicto) for c in db.session.query(Conflicto.ID_Conflicto).all()}
    new_conflictos = [
        Conflicto(
            ID_Conflicto=row['ID'],
            Tipo=row['Tipo'],
            ID_Comuna=row['ID_Comuna']
        ) for row in conflictos if row['ID'] not in existing_ids
    ]
    
    if new_conflictos:
        db.session.bulk_save_objects(new_conflictos)
        db.session.commit()
        print("Conflictos insertados correctamente.")
        logging.info("Conflictos insertados correctamente.")
    else:
        print("No hay nuevos conflictos para insertar.")
        logging.info("No hay nuevos conflictos para insertar.")

def insert_catastrofes(catastrofes):
    print("Iniciando la inserción de catástrofes...")
    logging.info("Iniciando la inserción de catástrofes...")
    
    existing_ids = {str(c.ID_Catastrofe) for c in db.session.query(Catastrofe.ID_Catastrofe).all()}
    new_catastrofes = [
        Catastrofe(
            ID_Catastrofe=row['ID'],
            Tipo=row['Tipo'],
            Frecuencia=row['Frecuencia'],
            ID_Comuna=row['ID_Comuna']
        ) for row in catastrofes if row['ID'] not in existing_ids
    ]
    
    if new_catastrofes:
        db.session.bulk_save_objects(new_catastrofes)
        db.session.commit()
        print("Catástrofes insertadas correctamente.")
        logging.info("Catástrofes insertadas correctamente.")
    else:
        print("No hay nuevas catástrofes para insertar.")
        logging.info("No hay nuevas catástrofes para insertar.")
