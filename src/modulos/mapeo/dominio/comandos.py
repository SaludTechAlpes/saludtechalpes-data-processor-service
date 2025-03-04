from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import List, Optional

import src.modulos.mapeo.dominio.objetos_valor as ov


@dataclass
class MapearDatosComando:
    id_imagen: Optional[uuid.UUID] = None
    etiquetas_patologicas: List[ov.EtiquetaPatologica] = field(default_factory=list)
    ruta_imagen_anonimizada: Optional[str] = None
