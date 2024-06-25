import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as PgEnum
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

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

    def to_json(self):
        return {
            'ID_Region': self.ID_Region,
            'Nombre': self.Nombre
        }

class Comuna(db.Model):
    __tablename__ = 'comuna'
    ID_Comuna = Column(Integer, primary_key=True)
    Nombre = Column(String)
    ID_Region = Column(Integer, ForeignKey('region.ID_Region'))
    region = relationship("Region", back_populates="comunas")

    def to_json(self):
        return {
            'ID_Comuna': self.ID_Comuna,
            'Nombre': self.Nombre,
            'ID_Region': self.ID_Region,
            'region': self.region.to_json() if self.region else None
        }

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

    def to_json(self):
        return {
            'ID_Escuela': self.ID_Escuela,
            'Nombre': self.Nombre,
            'ID_Comuna': self.ID_Comuna,
            'Infraestructura': self.Infraestructura.value,
            'Acceso_Educacion': self.Acceso_Educacion,
            'Finalizacion_Basica': self.Finalizacion_Basica,
            'Finalizacion_Media': self.Finalizacion_Media,
            'Mujeres_Acceso': self.Mujeres_Acceso,
            'Mujeres_Finalizacion': self.Mujeres_Finalizacion,
            'Acceso_Superior': self.Acceso_Superior,
            'Preparacion_Maestros': self.Preparacion_Maestros.value,
            'comuna': self.comuna.to_json() if self.comuna else None
        }

class Conflicto(db.Model):
    __tablename__ = 'conflicto'
    ID_Conflicto = Column(Integer, primary_key=True)
    Tipo = Column(String)
    ID_Comuna = Column(Integer, ForeignKey('comuna.ID_Comuna'))
    comuna = relationship("Comuna", back_populates="conflictos")

    def to_json(self):
        return {
            'ID_Conflicto': self.ID_Conflicto,
            'Tipo': self.Tipo,
            'ID_Comuna': self.ID_Comuna,
            'comuna': self.comuna.to_json() if self.comuna else None
        }

class Catastrofe(db.Model):
    __tablename__ = 'catastrofe'
    ID_Catastrofe = Column(Integer, primary_key=True)
    Tipo = Column(String)
    Frecuencia = Column(Integer)
    ID_Comuna = Column(Integer, ForeignKey('comuna.ID_Comuna'))
    comuna = relationship("Comuna", back_populates="catastrofes")

    def to_json(self):
        return {
            'ID_Catastrofe': self.ID_Catastrofe,
            'Tipo': self.Tipo,
            'Frecuencia': self.Frecuencia,
            'ID_Comuna': self.ID_Comuna,
            'comuna': self.comuna.to_json() if self.comuna else None
        }

# Establece relaciones inversas
Region.comunas = relationship("Comuna", order_by=Comuna.ID_Comuna, back_populates="region")
Comuna.escuelas = relationship("Escuela", order_by=Escuela.ID_Escuela, back_populates="comuna")
Comuna.conflictos = relationship("Conflicto", order_by=Conflicto.ID_Conflicto, back_populates="comuna")
Comuna.catastrofes = relationship("Catastrofe", order_by=Catastrofe.ID_Catastrofe, back_populates="comuna")
