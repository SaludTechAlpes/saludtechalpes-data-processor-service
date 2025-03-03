from abc import ABC, abstractmethod
from uuid import UUID

class PuertoProcesarComandoMapeo(ABC):
    @abstractmethod
    def procesar_comando_mapeo(self, id_imagen: UUID, etiquetas_patologicas: list[str], ruta_imagen_anonimizada: str):
        ...
