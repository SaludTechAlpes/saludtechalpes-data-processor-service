from pulsar.schema import *
from dataclasses import dataclass, field
from seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoAnonimizarDatosPayload(ComandoIntegracion):
    id_imagen = String()
    ruta_imagen = String()
    ruta_archivo_metadatos = String()

class ComandoAnonimizarDatos(ComandoIntegracion):
    data = ComandoAnonimizarDatosPayload()