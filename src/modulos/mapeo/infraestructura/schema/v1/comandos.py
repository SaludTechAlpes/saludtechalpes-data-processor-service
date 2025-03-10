from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoMapearDatosPayload(ComandoIntegracion):
    id_imagen_importada = String()
    id_imagen_anonimizada = String()
    etiquetas_patologicas = Array(String())
    ruta_imagen_anonimizada = String()
    evento_a_fallar = String()

class ComandoMapearDatos(ComandoIntegracion):
    data = ComandoMapearDatosPayload()

class ComandoRevetirMapeoPayload(ComandoIntegracion):
    id_imagen_mapeada = String()
    es_compensacion = Boolean()

class ComandoRevertirMapeoDatos(ComandoIntegracion):
    data = ComandoRevetirMapeoPayload()