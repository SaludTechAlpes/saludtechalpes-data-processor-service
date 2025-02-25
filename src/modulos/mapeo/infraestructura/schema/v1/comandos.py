from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from typing import List, Optional

class ComandoMapearDatosPayload(ComandoIntegracion):
    id_imagen = String()
    etiquetas_patologicas = List(String())

class ComandoMapearDatos(ComandoIntegracion):
    data = ComandoMapearDatosPayload()
