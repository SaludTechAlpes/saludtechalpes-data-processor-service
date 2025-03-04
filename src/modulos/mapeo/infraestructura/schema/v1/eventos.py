from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DatosMapeadosPayload(Record):
    cluster_id = String()
    ruta_imagen_anonimizada = String()

class EventoDatosMapeados(EventoIntegracion):
    data = DatosMapeadosPayload()
