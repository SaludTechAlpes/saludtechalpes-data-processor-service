import os
import pulsar
import json
import logging
import threading

from flask import Flask, jsonify, request
from src.config.config import Config

# Modulo de ingesta (Mock)
from src.modulos.ingesta.infraestructura.despachadores import DespachadorIngesta
from src.modulos.ingesta.dominio.eventos import DatosImportadosEvento

# Modulo de anonimización
from src.modulos.anonimizacion.infraestructura.despachadores import DespachadorAnonimizacion
from src.modulos.anonimizacion.dominio.comandos import RevertirAnonimizacionDatosComando
from src.modulos.anonimizacion.aplicacion.servicios import ServicioAplicacionAnonimizacion
from src.modulos.anonimizacion.infraestructura.adaptadores.anonimizar_datos import AdaptadorAnonimizarDatos
from src.modulos.anonimizacion.infraestructura.adaptadores.repositorios import RepositorioImagenAnonimizadaPostgres
from src.modulos.anonimizacion.infraestructura.consumidores_comandos import ConsumidorComandoAnonimizacion, ConsumidorComandoRevetirAnonimizacion
from src.modulos.anonimizacion.infraestructura.consumidores_eventos import ConsumidorEventosIngesta

# Modulo de mapeo
from src.modulos.mapeo.aplicacion.servicios import ServicioAplicacionMapeo
from src.modulos.mapeo.infraestructura.adaptadores.mapear_datos import AdaptadorMapearDatos
from src.modulos.mapeo.infraestructura.adaptadores.repositorios import RepositorioImagenMapeadaPostgres
from src.modulos.mapeo.infraestructura.consumidores_comandos import ConsumidorComandosMapeo
from src.modulos.mapeo.infraestructura.consumidores_eventos import ConsumidorEventosAnonimizacion

from src.config.db import Base, engine

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))
config = Config()

def comenzar_consumidor():
    """
    Inicia el consumidor en un hilo separado, pasando el servicio de aplicación.
    """

    if os.getenv("FLASK_ENV") == "test":
        logger.info("🔹 Saltando inicio de consumidores en modo test")
        return
    # Crear las dependencias del servicio de aplicación de anonimización
    adaptador_anonimizacion = AdaptadorAnonimizarDatos()
    repositorio_imagenes = RepositorioImagenAnonimizadaPostgres()
    
    # Instanciar el servicio de aplicación de anonimización con sus dependencias
    servicio_anonimizacion = ServicioAplicacionAnonimizacion(adaptador_anonimizacion, repositorio_imagenes)

    consumidor_eventos_ingesta = ConsumidorEventosIngesta()
    threading.Thread(target=consumidor_eventos_ingesta.suscribirse, daemon=True).start()
    
    consumidor_comando_anonimizacion = ConsumidorComandoAnonimizacion(servicio_anonimizacion)
    threading.Thread(target=consumidor_comando_anonimizacion.suscribirse, daemon=True).start()

    consumidor_comando_revertir_anonimizacion = ConsumidorComandoRevetirAnonimizacion(servicio_anonimizacion)
    threading.Thread(target=consumidor_comando_revertir_anonimizacion.suscribirse, daemon=True).start()

    # Crear las dependencias del servicio de aplicación de mapeo
    adaptador_mapeo = AdaptadorMapearDatos()
    repositorio_imagenes_mapeadas = RepositorioImagenMapeadaPostgres()

    # Instanciar el servicio de aplicación de mapeo con sus dependencias
    servicio_mapeo = ServicioAplicacionMapeo(adaptador_mapeo, repositorio_imagenes_mapeadas)

    # consumidor_eventos_anonimizacion = ConsumidorEventosAnonimizacion()
    # threading.Thread(target=consumidor_eventos_anonimizacion.suscribirse, daemon=True).start()

    # consumidor_comandos_mapeo = ConsumidorComandosMapeo(servicio_mapeo)
    # threading.Thread(target=consumidor_comandos_mapeo.suscribirse, daemon=True).start()

def create_app(configuracion=None):
    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        if app.config.get('TESTING'):
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        Base.metadata.create_all(engine) 
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    despachador_ingesta = DespachadorIngesta()

    

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }

    @app.route("/simular-ingesta-evento", methods=["POST"])
    def simular_ingesta_evento():
        """
        Endpoint para probar la publicación de comandos en Pulsar.
        """
        try:
            data = request.get_json()
            id_imagen_importada = data.get("id_imagen_importada", None)
            evento_a_fallar = data.get("evento_a_fallar", None)

            evento_prueba = DatosImportadosEvento(
                id_imagen_importada=id_imagen_importada,
                ruta_imagen_importada="/ruta/fake/imagen.dcm",
                ruta_metadatos_importados="/ruta/fake/metadatos.pdf",
                evento_a_fallar=evento_a_fallar
            )

            if not app.config.get('TESTING'):
                despachador_ingesta.publicar_evento(evento_prueba, "datos-importados")

            return jsonify({"message": "Evento publicado en `datos-importados`"}), 200
        except Exception as e:
            logger.error(f"❌ Error al enviar evento en `datos-importados`: {e}")
            return jsonify({"error": "Error al enviar evento en `datos-importados`"}), 500

    @app.route("/simular-anonimizacion-comando-compensacion", methods=["POST"])
    def simular_comando_compensacion():
        """
        Endpoint para simular el envio de una imagen desde el proveedor
        """
        try:
            data = request.get_json()
            id_imagen_anonimizada = data.get("id_imagen_anonimizada", None)

            despachador = DespachadorAnonimizacion()

            comando_compensacion = RevertirAnonimizacionDatosComando(
                id_imagen_anonimizada = id_imagen_anonimizada,
                es_compensacion = True
            )

            if not app.config.get('TESTING'):
                despachador.publicar_comando_compensacion(comando_compensacion, "revertir-anonimizar-datos")

            return jsonify({"message": "Evento de compensacion publicado en `revertir-anonimizar-datos`"}), 200
        
        except Exception as e:
            logger.error(f"❌ Error al publicar evento de compensación en `revertir-anonimizar-datos`: {e}")
            return jsonify({"error": "Error al publicar evento de compensacion en `revertir-anonimizar-datos`"}), 500

    return app
