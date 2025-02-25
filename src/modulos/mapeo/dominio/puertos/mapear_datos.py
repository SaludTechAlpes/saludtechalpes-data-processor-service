from abc import ABC, abstractmethod

class PuertoMapearDatos(ABC):
    @abstractmethod
    def mapear_datos(self, id_imagen: str, etiquetas_patologicas: list[str]) -> dict:
        ...
