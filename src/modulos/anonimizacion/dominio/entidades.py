from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from typing import List

import modulos.anonimizacion.dominio.objetos_valor as ov
from modulos.anonimizacion.dominio.eventos import DatosImportadosEvento
from seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class ImagenAnonimizada(AgregacionRaiz):
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    ruta_imagen_anonimizada: str
    fecha_procesamiento: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadatos: MetadatosAnonimizados

    def marcar_como_procesada(self):
        self.estado = ov.EstadoAnonimizacion.PROCESADO
        self.agregar_evento(DatosImportadosEvento(self.id, datetime.now(timezone.utc)))

@dataclass
class MetadatosAnonimizados(Entidad):
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    token_paciente: uuid.UUID = field(default_factory=uuid.uuid4)
    modalidad: ov.Modalidad
    region_anatomica: ov.RegionAnatomica
    fecha_estudio: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    etiquetas: List[ov.EtiquetaPatologica] = field(default_factory=list)
