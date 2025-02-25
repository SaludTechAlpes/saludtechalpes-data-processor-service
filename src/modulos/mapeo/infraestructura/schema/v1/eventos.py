from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DatosMapeadosPayload(Record):
    id_imagen_mapeada = String()

class EventoDatosMapeados(EventoIntegracion):
    data = DatosMapeadosPayload()
