import os
import pulsar
import json
import logging
import threading

from flask import Flask, jsonify
from config import Config
from modulos.ingesta.infraestructura.despachadores import Despachador
from modulos.ingesta.dominio.comandos import DatosImportadosComando
from modulos.anonimizacion.infraestructura.consumidores import ConsumidorComandosAnonimizacion
from modulos.anonimizacion.aplicacion.servicios import ServicioAplicacionAnonimizacion
from modulos.anonimizacion.infraestructura.adaptadores.anonimizar_datos import AdaptadorAnonimizarDatos
from modulos.anonimizacion.infraestructura.adaptadores.repositorios import RepositorioImagenAnonimizadaPostgres
from config.db import Base, engine

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))
config = Config()

pulsar_cliente = pulsar.Client('pulsar://broker:6650')

def comenzar_consumidor():
    """
    Inicia el consumidor en un hilo separado, pasando el servicio de aplicación.
    """

    # Crear las dependencias del servicio de aplicación
    adaptador_anonimizacion = AdaptadorAnonimizarDatos()
    repositorio_imagenes = RepositorioImagenAnonimizadaPostgres()
    
    # Instanciar el servicio de aplicación con sus dependencias
    servicio_anonimizacion = ServicioAplicacionAnonimizacion(adaptador_anonimizacion, repositorio_imagenes)
    
    # Instanciar el consumidor y pasarle el servicio de aplicación
    consumidor = ConsumidorComandosAnonimizacion(servicio_anonimizacion)

    # Ejecutar el consumidor en un hilo para no bloquear Flask
    threading.Thread(target=consumidor.suscribirse, daemon=True).start()

def create_app(configuracion=None):
    global pulsar_cliente

    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        Base.metadata.create_all(engine) 
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    despachador_ingesta = Despachador()

    

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }

    @app.route("/simular-ingesta-evento", methods=["GET"])
    def simular_ingesta_evento():
        """
        Endpoint para probar la publicación de comandos en Pulsar.
        """
        try:
            comando_prueba = DatosImportadosComando(
                ruta_imagen="/ruta/fake/imagen.dcm",
                ruta_metadatos="/ruta/fake/metadatos.pdf",
            )

            despachador_ingesta.publicar_comando(comando_prueba, "comandos-ingesta")

            return jsonify({"message": "Comando enviado a Pulsar"}), 200
        except Exception as e:
            logger.error(f"Error al enviar comando de prueba: {e}")
            return jsonify({"error": "Error al enviar comando a Pulsar"}), 500

    

    # Cerrar Pulsar cuando la aplicación termina
    @app.teardown_appcontext
    def cerrar_pulsar(exception=None):
        global pulsar_cliente
        if pulsar_cliente:
            pulsar_cliente.close()
            logger.info("Cliente Pulsar cerrado al detener Flask.")

    return app
