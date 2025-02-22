from abc import ABC, abstractmethod
from uuid import UUID

class PuertoProcesarEventoAnonimizacion(ABC):
    @abstractmethod
    def procesar_evento_anonimizacion(self, id_imagen: UUID, ruta_imagen: str):
        ...
