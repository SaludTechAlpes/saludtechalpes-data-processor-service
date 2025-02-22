import pulsar
from pulsar.schema import AvroSchema
import json
import logging
from modulos.anonimizacion.infraestructura.schema.v1.eventos import DatosAnonimizadosPayload, EventoDatosAnonimizados
from modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoAnonimizarDatosPayload, ComandoAnonimizarDatos
from seedwork.infraestructura import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        try:
            cliente = pulsar.Client('pulsar://broker:6650')
            logger.info(f"Publicando mensaje en {topico}: {mensaje}")
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
            publicador.send(mensaje)
            logger.info(f"Mensaje publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"Error publicando mensaje en {topico}: {e}")


    def publicar_evento(self, evento, topico):
        payload = DatosAnonimizadosPayload(
            id_imagen=str(evento.id_imagen),
            ruta_imagen_anonimizada=evento.ruta_imagen_anonimizada,
            id_paciente=str(evento.id_paciente),
            modalidad=evento.modalidad,
            region_anatomica=evento.region_anatomica,
            fecha_estudio=int(evento.fecha_estudio.timestamp() * 1000),
            etiquetas_patologicas=evento.etiquetas_patologicas
        )
        evento_gordo=EventoDatosAnonimizados(data=payload)
        self._publicar_mensaje(evento_gordo, topico, EventoDatosAnonimizados)

    def cerrar(self):
        self.cliente.close()
        logger.info("Cliente Pulsar cerrado.")
