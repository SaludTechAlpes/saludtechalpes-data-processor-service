from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DatosMapeadosPayload(Record):
    id_imagen = String()
    id_cluster_patologia = String()

class EventoDatosMapeados(EventoIntegracion):
    data = DatosMapeadosPayload()
