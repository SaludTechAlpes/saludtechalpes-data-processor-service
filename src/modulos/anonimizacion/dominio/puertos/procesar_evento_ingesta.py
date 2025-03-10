from abc import ABC, abstractmethod
from uuid import UUID

class PuertoProcesarEventoIngesta(ABC):
    @abstractmethod
    def procesar_evento_ingesta(self, ruta_imagen_importada: str, ruta_metadatos_importados: str):
        ...
