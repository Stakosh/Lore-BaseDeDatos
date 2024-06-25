from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as PgEnum
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()

# Definir las enumeraciones
class InfraestructuraEnum(enum.Enum):
    Buena = 'Buena'
    Media = 'Media'
    Mala = 'Mala'

class PreparacionMaestrosEnum(enum.Enum):
    Alto = 'Alto'
    Bajo = 'Bajo'

class Region(db.Model):
    __tablename__ = 'region'
    ID_Region = Column(Integer, primary_key=True)
    Nombre = Column(String)

class Comuna(db.Model):
    __tablename__ = 'comuna'
    ID_Comuna = Column(Integer, primary_key=True)
    Nombre = Column(String)
    ID_Region = Column(Integer, ForeignKey('region.ID_Region'))
    region = relationship("Region", back_populates="comunas")

class Escuela(db.Model):
    __tablename__ = 'escuela'
    ID_Escuela = Column(Integer, primary_key=True)
    Nombre = Column(String)
    ID_Comuna = Column(Integer, ForeignKey('comuna.ID_Comuna'))
    Infraestructura = Column(PgEnum(InfraestructuraEnum, name="infraestructura_enum"))
    Acceso_Educacion = Column(Integer)
    Finalizacion_Basica = Column(Integer)
    Finalizacion_Media = Column(Integer)
    Mujeres_Acceso = Column(Integer)
    Mujeres_Finalizacion = Column(Integer)
    Acceso_Superior = Column(Integer)
    Preparacion_Maestros = Column(PgEnum(PreparacionMaestrosEnum, name="preparacion_maestros_enum"))
    comuna = relationship("Comuna", back_populates="escuelas")

class Conflicto(db.Model):
    __tablename__ = 'conflicto'
    ID_Conflicto = Column(Integer, primary_key=True)
    Tipo = Column(String)
    ID_Comuna = Column(Integer, ForeignKey('comuna.ID_Comuna'))
    comuna = relationship("Comuna", back_populates="conflictos")

class Catastrofe(db.Model):
    __tablename__ = 'catastrofe'
    ID_Catastrofe = Column(Integer, primary_key=True)
    Tipo = Column(String)
    Frecuencia = Column(Integer)
    ID_Comuna = Column(Integer, ForeignKey('comuna.ID_Comuna'))
    comuna = relationship("Comuna", back_populates="catastrofes")

# Establece relaciones inversas
Region.comunas = relationship("Comuna", order_by=Comuna.ID_Comuna, back_populates="region")
Comuna.escuelas = relationship("Escuela", order_by=Escuela.ID_Escuela, back_populates="comuna")
Comuna.conflictos = relationship("Conflicto", order_by=Conflicto.ID_Conflicto, back_populates="comuna")
Comuna.catastrofes = relationship("Catastrofe", order_by=Catastrofe.ID_Catastrofe, back_populates="comuna")
