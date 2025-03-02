from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoMapearDatosPayload(ComandoIntegracion):
    id_imagen = String()
    etiquetas_patologicas = Array(String())
    ruta_imagen_anonimizada = String()

class ComandoMapearDatos(ComandoIntegracion):
    data = ComandoMapearDatosPayload()
