from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from src.config.db import Base
import uuid
import os
import json

def get_uuid():
    return str(uuid.uuid4())

def default_list():
    return []

class ImagenAnonimizadaDTO(Base):    
    __tablename__ = "imagenes_anonimizadas"

    if os.getenv("FLASK_ENV") == "test":
        id = Column(String, primary_key=True, default=get_uuid)
        metadatos_id = Column(String, ForeignKey("metadatos_anonimizados.id",ondelete="CASCADE"), nullable=True)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        metadatos_id = Column(UUID(as_uuid=True), ForeignKey("metadatos_anonimizados.id", ondelete="CASCADE"), nullable=True)

    ruta_imagen_anonimizada = Column(String, nullable=False)
    fecha_procesamiento = Column(DateTime, nullable=False)
    metadatos = relationship("MetadatosAnonimizadosDTO", back_populates="imagen", cascade="all, delete")


class MetadatosAnonimizadosDTO(Base):  
    __tablename__ = "metadatos_anonimizados"

    if os.getenv("FLASK_ENV") == "test":
        id = Column(String, primary_key=True, default=get_uuid)
        token_paciente = Column(String, nullable=False)
        etiquetas = Column(String, nullable=True)  # Se almacena como JSON en SQLite
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        token_paciente = Column(UUID(as_uuid=True), nullable=False)
        etiquetas = Column(MutableList.as_mutable(ARRAY(String)), nullable=True, default=default_list)  # 🔹 Se usa una función para el default

    modalidad = Column(String, nullable=True)
    region_anatomica = Column(String, nullable=True)
    fecha_estudio = Column(DateTime, nullable=False)
    imagen = relationship("ImagenAnonimizadaDTO", back_populates="metadatos")

    def set_etiquetas(self, etiquetas_list):
        if os.getenv("FLASK_ENV") == "test":
            self.etiquetas = json.dumps(etiquetas_list)
        else:
            self.etiquetas = etiquetas_list

    def get_etiquetas(self):
        if os.getenv("FLASK_ENV") == "test":
            return json.loads(self.etiquetas) if self.etiquetas else []
        return self.etiquetas
