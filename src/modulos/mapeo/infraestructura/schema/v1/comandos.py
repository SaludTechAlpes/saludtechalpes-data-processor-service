from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoMapearDatosPayload(ComandoIntegracion):
    id_imagen = String()
    ruta_imagen = String()
    id_paciente = String()
    modalidad = String()
    region_anatomica = String()
    fecha_estudio = String()
    etiquetas_patologicas = String()

class ComandoMapearDatos(ComandoIntegracion):
    data = ComandoMapearDatosPayload()