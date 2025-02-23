from sqlalchemy import Column, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.db import Base
import uuid

class ImagenAnonimizadaDTO(Base):    
    __tablename__ = "imagenes_anonimizadas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ruta_imagen_anonimizada = Column(String, nullable=False)
    fecha_procesamiento = Column(DateTime, nullable=False)
    metadatos_id = Column(UUID(as_uuid=True), ForeignKey("metadatos_anonimizados.id", ondelete="SET NULL"), nullable=True)
    metadatos = relationship("MetadatosAnonimizadosDTO", back_populates="imagen")

class MetadatosAnonimizadosDTO(Base):  
    __tablename__ = "metadatos_anonimizados"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_paciente = Column(UUID(as_uuid=True), nullable=False)
    modalidad = Column(String, nullable=True)
    region_anatomica = Column(String, nullable=True)
    fecha_estudio = Column(DateTime, nullable=False)
    etiquetas = Column(ARRAY(String), nullable=True, default=[])
    imagen = relationship("ImagenAnonimizadaDTO", back_populates="metadatos")