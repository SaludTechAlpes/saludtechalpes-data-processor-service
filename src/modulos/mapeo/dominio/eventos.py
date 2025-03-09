from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime
from typing import List, Optional
from src.seedwork.dominio.eventos import EventoDominio
import src.modulos.mapeo.dominio.objetos_valor as ov


@dataclass
class DatosAgrupadosEvento(EventoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    id_imagen_mapeada: Optional[uuid.UUID] = None
    cluster_id: Optional[uuid.UUID] = None
    ruta_imagen_anonimizada: Optional[str] = None
    evento_a_fallar: Optional[str] = None

@dataclass
class DatosAgrupadosEventoFallido(EventoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    id_imagen_mapeada: Optional[uuid.UUID] = None
