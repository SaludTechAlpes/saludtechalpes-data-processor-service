from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoAnonimizarDatosPayload(ComandoIntegracion):
    id_imagen_importada = String()
    ruta_imagen_importada = String()
    ruta_metadatos_importados = String()
    evento_a_fallar = String()

class ComandoAnonimizarDatos(ComandoIntegracion):
    data = ComandoAnonimizarDatosPayload()

class ComandoRevetirAnonimizacionDatosPayload(ComandoIntegracion):
    id_imagen_anonimizada = String()
    es_compensacion = Boolean()

class ComandoRevertirAnonimizacionDatos(ComandoIntegracion):
    data = ComandoRevetirAnonimizacionDatosPayload()