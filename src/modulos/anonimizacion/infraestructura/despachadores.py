import pulsar
import json
import logging
from modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoDatosAnonimizados
from modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoAnonimizarDatos
from seedwork.infraestructura import utils
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Despachador:
    def __init__(self):
        self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
    
    def _publicar_mensaje(self, mensaje, topico):
        try:
            logger.info(f"Publicando mensaje en {topico}: {mensaje}")
            publicador = self.cliente.create_producer(topico)
            publicador.send(json.dumps(mensaje).encode('utf-8'))
            logger.info(f"Mensaje publicado con éxito en {topico}")
        except Exception as e:
            logger.error(f"Error publicando mensaje en {topico}: {e}")
        finally:
            publicador.close()

    def publicar_evento(self, evento, topico):
        payload = {
            "id_imagen": str(evento.id_imagen),
            "ruta_imagen_anonimizada": evento.ruta_imagen_anonimizada,
            "id_paciente": str(evento.id_paciente),
            "modalidad": evento.modalidad,
            "region_anatomica": evento.region_anatomica,
            "fecha_estudio": evento.fecha_estudio.isoformat(),  # 🔹 Convertimos a ISO-8601
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

    def cerrar(self):
        self.cliente.close()
        logger.info("Cliente Pulsar cerrado.")
