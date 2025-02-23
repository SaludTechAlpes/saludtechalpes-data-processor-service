from abc import ABC, abstractmethod
from uuid import UUID

class PuertoProcesarComandoAnonimizacion(ABC):
    @abstractmethod
    def procesar_comando_anonimizacion(self, ruta_imagen: str, ruta_metadatos: str):
        ...
