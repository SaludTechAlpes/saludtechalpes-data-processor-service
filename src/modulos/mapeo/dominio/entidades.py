from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from typing import List

import src.modulos.mapeo.dominio.objetos_valor as ov
from src.seedwork.dominio.entidades import Entidad

@dataclass
class ImagenMapeada(Entidad):
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    imagen_mapeada_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id_cluster_patologia: uuid.UUID = field(default_factory=uuid.uuid4)
