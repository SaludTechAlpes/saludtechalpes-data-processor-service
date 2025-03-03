from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime
from typing import List, Optional
from src.seedwork.dominio.eventos import EventoDominio
import src.modulos.mapeo.dominio.objetos_valor as ov


@dataclass
class DatosMapeadosEvento(EventoDominio):
    id_imagen: Optional[uuid.UUID] = None
    id_cluster_patologia: Optional[uuid.UUID] = None
