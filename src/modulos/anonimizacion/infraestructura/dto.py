from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from modulos.anonimizacion.infraestructura.db import Base
import uuid

class ImagenAnonimizadaDTO(Base):
    """Representación de la entidad `ImagenAnonimizada` en la base de datos."""
    
    __tablename__ = "imagenes_anonimizadas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ruta_imagen_anonimizada = Column(String, nullable=False)
    fecha_procesamiento = Column(DateTime, nullable=False)
    estado = Column(String, nullable=False)
