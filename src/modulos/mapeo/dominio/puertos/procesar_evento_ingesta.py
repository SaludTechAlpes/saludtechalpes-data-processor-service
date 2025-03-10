from abc import ABC, abstractmethod
from uuid import UUID

class PuertoProcesarEventoAnonimizacion(ABC):
    @abstractmethod
    def procesar_evento_anonimizacion(self, ruta_imagen_importada: str, ruta_metadatos_importados: str):
        ...
