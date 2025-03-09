from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from src.seedwork.dominio.comandos import ComandoDominio


@dataclass
class AnonimizarDatosComando(ComandoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    ruta_imagen_importada: Optional[str] = None
    ruta_metadatos_importados:Optional[str] = None
    evento_a_fallar: Optional[str] = None

@dataclass
class RevertirAnonimizacionDatosComando(ComandoDominio):
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    es_compensacion: Optional[bool] = True
    
    
