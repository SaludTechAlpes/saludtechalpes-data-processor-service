from abc import ABC, abstractmethod
from uuid import UUID

class PuertoProcesarComandoMapeo(ABC):
    @abstractmethod
    def procesar_comando_mapeo(self, id_imagen: UUID, ruta_imagen_anonimizada: str, id_paciente: UUID, modalidad: str, region_anatomica: str, fecha_estudio: str, etiquetas_patologicas: list):
        ...
