from abc import ABC, abstractmethod
from uuid import UUID

class PuertoProcesarComandoMapeo(ABC):
    @abstractmethod
    def procesar_comando_mapeo(self, id_imagen_anonimizada: UUID, id_imagen_importada: UUID, etiquetas_patologicas: list[str], ruta_imagen_anonimizada: str, evento_a_fallar: str):
        ...
        
    @abstractmethod
    def procesar_comando_revertir_mapeo(self, id_imagen_mapeada: UUID):
        ...