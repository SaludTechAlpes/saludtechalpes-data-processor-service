from abc import ABC, abstractmethod
from uuid import UUID

class PuertoAnonimizacion(ABC):
    @abstractmethod
    def anonimizar_datos(self, ruta_imagen: str, ruta_archivo_metadatos: str) -> dict:
        ...
