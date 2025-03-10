import pulsar
from pulsar.schema import AvroSchema
import json
import logging
from src.modulos.anonimizacion.infraestructura.schema.v1.eventos import DatosAnonimizadosPayload, EventoDatosAnonimizados, DatosAnonimizadosFallidoPayload, EventoDatosAnonimizadosFallido
from src.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoAnonimizarDatosPayload, ComandoAnonimizarDatos, ComandoRevetirAnonimizacionDatosPayload, ComandoRevertirAnonimizacionDatos
from src.seedwork.infraestructura import utils
from src.config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config()

class DespachadorAnonimizacion:
    def _publicar_mensaje(self, mensaje, topico, schema):
        try:
            cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')
            logger.info(f"📤 Publicando mensaje en {topico}: {mensaje.data}")
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
            publicador.send(mensaje)
            logger.info(f"✅ Mensaje publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"❌ Error publicando mensaje en {topico}: {e}")


    def publicar_evento(self, evento, topico):
        payload = DatosAnonimizadosPayload(
            id_imagen_importada=str(evento.id_imagen_importada),
            id_imagen_anonimizada=str(evento.id_imagen_anonimizada),
            ruta_imagen_anonimizada=evento.ruta_imagen_anonimizada,
            id_paciente=str(evento.id_paciente),
            modalidad=evento.modalidad,
            region_anatomica=evento.region_anatomica,
            fecha_estudio=int(evento.fecha_estudio.timestamp() * 1000),
            etiquetas_patologicas=evento.etiquetas_patologicas,
            evento_a_fallar=evento.evento_a_fallar
        )
        evento_gordo=EventoDatosAnonimizados(data=payload)
        self._publicar_mensaje(evento_gordo, topico, EventoDatosAnonimizados)


    def publicar_evento_fallido(self, evento, topico):
        payload = DatosAnonimizadosFallidoPayload(
            id_imagen_importada=str(evento.id_imagen_importada),
            id_imagen_anonimizada=str(evento.id_imagen_anonimizada),
        )
        evento_gordo=EventoDatosAnonimizadosFallido(data=payload)
        self._publicar_mensaje(evento_gordo, topico, EventoDatosAnonimizadosFallido)

    def publicar_comando(self, evento, topico):
        payload = ComandoAnonimizarDatosPayload(
            id_imagen_importada=evento.id_imagen_importada,
            ruta_imagen_importada=evento.ruta_imagen_importada,
            ruta_metadatos_importados=evento.ruta_metadatos_importados,
            evento_a_fallar=evento.evento_a_fallar
        )
        evento_gordo=ComandoAnonimizarDatos(data=payload)
        self._publicar_mensaje(evento_gordo, topico, ComandoAnonimizarDatos)


    def publicar_comando_compensacion(self, evento, topico):
        payload = ComandoRevetirAnonimizacionDatosPayload(
            id_imagen_anonimizada=evento.id_imagen_anonimizada,
            es_compensacion=True
        )
        evento_gordo=ComandoRevertirAnonimizacionDatos(data=payload)
        self._publicar_mensaje(evento_gordo, topico, ComandoRevertirAnonimizacionDatos)

    def cerrar(self):
        self.cliente.close()
        logger.info("Cliente Pulsar cerrado.")
