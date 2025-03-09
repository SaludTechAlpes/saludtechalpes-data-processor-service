from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class AnonimizarDatosComando():
    id_imagen_importada: Optional[uuid.UUID] = None
    ruta_imagen_importada: Optional[str] = None
    ruta_metadatos_importados:Optional[str] = None
    evento_a_fallar: Optional[str] = None

@dataclass
class RevertirAnonimizacionDatosComando():
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    es_compensacion: Optional[bool] = True
    
    
