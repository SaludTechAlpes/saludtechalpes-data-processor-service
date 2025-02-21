import pulsar
import json
from modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoDatosAnonimizados, DatosAnonimizadosPayload
from modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoAnonimizarDatos, ComandoAnonimizarDatosPayload
from seedwork.infraestructura import utils
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return int((dt - epoch).total_seconds() * 1000.0)

class Despachador:
    def _publicar_mensaje(self, mensaje, topico):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico)
        publicador.send(json.dumps(mensaje).encode('utf-8'))
        cliente.close()

    def publicar_evento(self, evento, topico):
        payload = {
            "id_imagen": str(evento.id_imagen),
            "ruta_imagen_anonimizada": evento.ruta_imagen_anonimizada,
            "id_paciente": str(evento.id_paciente),
            "modalidad": evento.modalidad,
            "region_anatomica": evento.region_anatomica,
            "fecha_estudio": unix_time_millis(evento.fecha_estudio),
            "etiquetas_patologicas": evento.etiquetas_patologicas
        }
        self._publicar_mensaje(payload, topico)

    def publicar_comando(self, comando, topico):
        payload = {
            "id_imagen": str(comando.id_imagen),
            "ruta_imagen": comando.ruta_imagen,
            "ruta_metadatos": comando.ruta_metadatos
        }
        self._publicar_mensaje(payload, topico)
