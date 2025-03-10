from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from typing import List

import src.modulos.mapeo.dominio.objetos_valor as ov
from src.seedwork.dominio.entidades import Entidad

@dataclass
class ImagenMapeada(Entidad):
    id: uuid.UUID = None
    id_cluster_patologia: uuid.UUID = field(default_factory=uuid.uuid4)
    ruta_imagen_anonimizada: str = ""