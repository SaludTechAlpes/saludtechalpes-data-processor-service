"""Reglas de negocio del dominio de Anonimización

En este archivo encontrará reglas de negocio del dominio de anonimización.
"""

from seedwork.dominio.reglas import ReglaNegocio
from modulos.anonimizacion.dominio.objetos_valor import EtiquetaPatologica

class FormatoImagenValido(ReglaNegocio):
    """Regla de negocio para validar que la imagen tiene el formato correcto."""

    def __init__(self, ruta_imagen, mensaje="El formato de la imagen no es válido"):
        super().__init__(mensaje)
        self.ruta_imagen = ruta_imagen

    def es_valido(self) -> bool:
        return self.ruta_imagen.endswith((".dicom", ".dcm"))