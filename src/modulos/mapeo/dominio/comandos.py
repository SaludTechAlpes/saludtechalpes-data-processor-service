from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class MapearDatosComando():
    id_imagen: Optional[uuid.UUID] = None
    ruta_imagen_anonimizada: Optional[str] = None
    id_paciente: Optional[uuid.UUID] = None
    modalidad: Optional[ov.Modalidad] = None
    region_anatomica: Optional[ov.RegionAnatomica] = None
    fecha_estudio: Optional[datetime] = None
    etiquetas_patologicas: List[ov.EtiquetaPatologica] = field(default_factory=list) 



    
    
