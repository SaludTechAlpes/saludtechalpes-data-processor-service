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

class ImagenMapeadaDTO(Base):    
    __tablename__ = "imagenes_mapeadas"

    if os.getenv("FLASK_ENV") == "test":
        id = Column(String, primary_key=True, default=get_uuid)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    id_cluster_patologia = Column(String)
    ruta_imagen_anonimizada = Column(String)

