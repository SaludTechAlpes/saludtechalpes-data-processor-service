from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatosImportadosComando():
    id_imagen_importada: Optional[str] = None
    ruta_imagen_importada: Optional[str] = None
    ruta_metadatos_importados:Optional[str] = None
    evento_a_fallar:Optional[str] = None



    
    
