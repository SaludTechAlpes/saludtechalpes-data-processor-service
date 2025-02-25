import json
import logging

import pulsar
from pulsar.schema import AvroSchema

from src.modulos.mapeo.infraestructura.schema.v1.comandos import (
    ComandoMapearDatos,
    ComandoMapearDatosPayload,
)
from src.modulos.mapeo.infraestructura.schema.v1.eventos import (
    DatosMapeadosPayload,
    EventoDatosMapeados,
)
from src.seedwork.infraestructura import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        try:
            cliente = pulsar.Client("pulsar://broker:6650")
            logger.info(f"Publicando mensaje en {topico}: {mensaje}")
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
            publicador.send(mensaje)
            logger.info(f"Mensaje publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"Mensaje publicando mensaje en {topico}: {e}")

    def publicar_evento(self, evento, topico):
        payload = DatosMapeadosPayload(
            id_imagen_mapeada=str(evento.id_imagen_mapeada),
        )
        evento_gordo = EventoDatosMapeados(data=payload)
        self._publicar_mensaje(evento_gordo, topico, EventoDatosMapeados)

    def publicar_comando(self, evento, topico):
        payload = ComandoMapearDatosPayload(
            id_imagen=str(evento.id_imagen),
            etiquetas_patologicas=evento.etiquetas_patologicas,
        )
        evento_gordo = ComandoMapearDatos(data=payload)
        self._publicar_mensaje(evento_gordo, topico, ComandoMapearDatos)

    def cerrar(self):
        self.cliente.close()
        logger.info("Cliente Pulsar cerrado.")
