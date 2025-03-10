import json
import logging

import pulsar
from pulsar.schema import AvroSchema

from src.config.config import Config
from src.modulos.mapeo.infraestructura.schema.v1.comandos import (
    ComandoMapearDatos,
    ComandoMapearDatosPayload,
    ComandoRevetirMapeoPayload,
    ComandoRevertirMapeoDatos
)
from src.modulos.mapeo.infraestructura.schema.v1.eventos import (
    DatosAgrupadosPayload,
    EventoDatosAgrupados,
    DatosAgrupadosFallidoPayload,
    EventoDatosAgrupadosFallido
)
from src.seedwork.infraestructura import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Config()


class DespachadorMapeo:
    def _publicar_mensaje(self, mensaje, topico, schema):
        try:
            cliente = pulsar.Client(f"pulsar://{config.BROKER_HOST}:6650")
            logger.info(f"📤 Publicando mensaje en {topico}: {mensaje.data}")
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
            publicador.send(mensaje)
            logger.info(f"✅ Mensaje publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"❌ Error publicando mensaje en {topico}: {e}")

    def publicar_evento(self, evento, topico):
        payload = DatosAgrupadosPayload(
            id_imagen_importada = str(evento.id_imagen_importada),
            id_imagen_anonimizada = str(evento.id_imagen_anonimizada),
            id_imagen_mapeada = str(evento.id_imagen_mapeada),
            cluster_id=str(evento.cluster_id),
            ruta_imagen_anonimizada=evento.ruta_imagen_anonimizada,
            evento_a_fallar = evento.evento_a_fallar
        )
        evento_gordo = EventoDatosAgrupados(data=payload)
        self._publicar_mensaje(evento_gordo, topico, EventoDatosAgrupados)
    
    def publicar_evento_fallido(self, evento, topico):
        payload = DatosAgrupadosFallidoPayload(
            id_imagen_importada=str(evento.id_imagen_importada),
            id_imagen_anonimizada=str(evento.id_imagen_anonimizada),
            id_imagen_mapeada=str(evento.id_imagen_mapeada),
        )
        evento_gordo=EventoDatosAgrupadosFallido(data=payload)
        self._publicar_mensaje(evento_gordo, topico, EventoDatosAgrupadosFallido)

    def publicar_comando(self, evento, topico):
        payload = ComandoMapearDatosPayload(
            id_imagen_importada=str(evento.id_imagen_importada),
            id_imagen_anonimizada=str(evento.id_imagen_anonimizada),
            etiquetas_patologicas=evento.etiquetas_patologicas,
            ruta_imagen_anonimizada=evento.ruta_imagen_anonimizada,
            evento_a_fallar=evento.evento_a_fallar
        )
        evento_gordo = ComandoMapearDatos(data=payload)
        self._publicar_mensaje(evento_gordo, topico, ComandoMapearDatos)
        
    def publicar_comando_compensacion(self, evento, topico):
        payload = ComandoRevetirMapeoPayload(
            id_imagen_mapeada=evento.id_imagen_mapeada,
            es_compensacion=True
        )
        evento_gordo=ComandoRevertirMapeoDatos(data=payload)
        self._publicar_mensaje(evento_gordo, topico, ComandoRevertirMapeoDatos)

    def cerrar(self):
        self.cliente.close()
        logger.info("Cliente Pulsar cerrado.")
