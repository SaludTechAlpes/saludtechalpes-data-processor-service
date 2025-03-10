from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from typing import List

import src.modulos.anonimizacion.dominio.objetos_valor as ov
from src.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class ImagenAnonimizada(AgregacionRaiz):
    id: uuid.UUID = None
    ruta_imagen_anonimizada: str = ""
    fecha_procesamiento: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadatos: MetadatosAnonimizados = field(default_factory=lambda: MetadatosAnonimizados(
        modalidad=ov.Modalidad.DEFAULT,
        region_anatomica=ov.RegionAnatomica.DEFAULT
    ))


@dataclass
class MetadatosAnonimizados(Entidad):
    id: uuid.UUID = None
    token_paciente: uuid.UUID = field(default_factory=uuid.uuid4)
    modalidad: ov.Modalidad = ov.Modalidad.DEFAULT
    region_anatomica: ov.RegionAnatomica = ov.RegionAnatomica.DEFAULT
    fecha_estudio: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    etiquetas: List[ov.EtiquetaPatologica] = field(default_factory=list)
