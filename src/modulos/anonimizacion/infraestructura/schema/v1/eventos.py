from pulsar.schema import *
from seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DatosAnonimizadosPayload(Record):
    id_imagen = String()
    ruta_imagen_anonimizada = String()
    id_paciente = String()
    modalidad = String()
    region_anatomica = String()
    fecha_estudio = Long()
    etiquetas_patologicas = Array(String())

class EventoDatosAnonimizados(EventoIntegracion):
    data = DatosAnonimizadosPayload()
