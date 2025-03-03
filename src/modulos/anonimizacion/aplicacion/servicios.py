from src.modulos.anonimizacion.dominio.puertos.procesar_comando_anonimizacion import PuertoProcesarComandoAnonimizacion
from src.modulos.anonimizacion.dominio.servicios import ServicioDominioAnonimizacion
from src.modulos.anonimizacion.dominio.entidades import ImagenAnonimizada, MetadatosAnonimizados
from src.modulos.anonimizacion.infraestructura.adaptadores.anonimizar_datos import AdaptadorAnonimizarDatos
from src.modulos.anonimizacion.dominio.puertos.repositorios import RepositorioImagenAnonimizada
from src.modulos.anonimizacion.infraestructura.despachadores import Despachador
from src.modulos.anonimizacion.dominio.eventos import DatosAnonimizadosEvento
import uuid
from datetime import datetime, timezone
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServicioAplicacionAnonimizacion(PuertoProcesarComandoAnonimizacion):
    def __init__(self, adaptador_anonimizacion: AdaptadorAnonimizarDatos, repositorio_imagenes: RepositorioImagenAnonimizada):
        self.adaptador_anonimizacion = adaptador_anonimizacion
        self.repositorio_imagenes = repositorio_imagenes
        self.servicio_dominio = ServicioDominioAnonimizacion()
        self.despachador = Despachador()

    def procesar_comando_anonimizacion(self, ruta_imagen: str, ruta_metadatos: str):
        try:
            self.servicio_dominio.validar_imagen(ruta_imagen)

            datos_anonimizados = self.adaptador_anonimizacion.anonimizar_datos(ruta_imagen, ruta_metadatos)

            if not datos_anonimizados:
                raise ValueError("Error: No se pudo anonimizar la imagen")
            
            logger.info(f'👉 Datos_anonimizados: {datos_anonimizados}')

            metadatos_anonimizados = MetadatosAnonimizados(
                id=uuid.uuid4(),
                token_paciente=uuid.uuid4(),
                modalidad=datos_anonimizados["metadatos_anonimizados"]["modalidad"],
                region_anatomica=datos_anonimizados["metadatos_anonimizados"]["region_anatomica"],
                fecha_estudio=datos_anonimizados["metadatos_anonimizados"]["fecha_estudio"],
                etiquetas=datos_anonimizados["metadatos_anonimizados"]["etiquetas"]
            )

            id_imagen=uuid.uuid4()
            imagen_anonimizada = ImagenAnonimizada(
                id=id_imagen,
                ruta_imagen_anonimizada=datos_anonimizados["ruta_imagen_anonimizada"],
                fecha_procesamiento=datetime.now(timezone.utc),
                metadatos=metadatos_anonimizados
            )

            self.repositorio_imagenes.agregar(imagen_anonimizada)

            evento = DatosAnonimizadosEvento(
                id_imagen=id_imagen,
                ruta_imagen_anonimizada=imagen_anonimizada.ruta_imagen_anonimizada,
                id_paciente=imagen_anonimizada.metadatos.token_paciente,
                modalidad=imagen_anonimizada.metadatos.modalidad,
                region_anatomica=imagen_anonimizada.metadatos.region_anatomica,
                fecha_estudio=imagen_anonimizada.metadatos.fecha_estudio,
                etiquetas_patologicas=imagen_anonimizada.metadatos.etiquetas,
            )

            self.despachador.publicar_evento(evento, 'datos-anonimizados')
            logger.info(f"👉 Imagen {id_imagen} anonimizada y evento publicado al topico datos-anonimizados: {evento}")

        except Exception as e:
            logger.error(f"❌ Error al anonimizar la imagen: {e}")
            raise
