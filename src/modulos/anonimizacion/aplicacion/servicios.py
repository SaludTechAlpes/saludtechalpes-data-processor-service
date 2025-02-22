from modulos.anonimizacion.dominio.puertos import PuertoAplicacionAnonimizacion
from modulos.anonimizacion.dominio.servicios import ServicioDominioAnonimizacion
from modulos.anonimizacion.dominio.entidades import ImagenAnonimizada, MetadatosAnonimizados
from modulos.anonimizacion.infraestructura.adaptadores import AdaptadorAnonimizacion
from modulos.anonimizacion.dominio.repositorios import RepositorioImagenAnonimizada
from modulos.anonimizacion.infraestructura.despachadores import Despachador
from modulos.anonimizacion.dominio.eventos import DatosAnonimizadosEvento
import uuid
from datetime import datetime, timezone
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServicioAplicacionAnonimizacion(PuertoAplicacionAnonimizacion):
    def __init__(self, adaptador_anonimizacion: AdaptadorAnonimizacion, repositorio_imagenes: RepositorioImagenAnonimizada):
        self.adaptador_anonimizacion = adaptador_anonimizacion
        self.repositorio_imagenes = repositorio_imagenes
        self.despachador = Despachador()

    def procesar_evento_anonimizacion(self, id_imagen: uuid.UUID, ruta_imagen: str):
        try:
            ServicioDominioAnonimizacion.validar_imagen(ruta_imagen)

            datos_anonimizados = self.adaptador_anonimizacion.anonimizar_datos(ruta_imagen, "")

            if not datos_anonimizados:
                raise ValueError(f"Error: No se pudo anonimizar la imagen {id_imagen}")

            metadatos_anonimizados = MetadatosAnonimizados(
                id=uuid.uuid4(),
                token_paciente=uuid.uuid4(),
                modalidad=datos_anonimizados["metadatos_anonimizados"]["modalidad"],
                region_anatomica=datos_anonimizados["metadatos_anonimizados"]["region_anatomica"],
                fecha_estudio=datetime.now(timezone.utc),
                etiquetas=datos_anonimizados["metadatos_anonimizados"]
            )

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
                fecha=datetime.now(timezone.utc)
            )

            self.despachador.publicar_evento(evento, 'eventos-anonimizacion')
            logger.info(f"Imagen {id_imagen} anonimizada y evento publicado")

        except Exception as e:
            logger.error(f"Error al anonimizar la imagen {id_imagen}: {e}")
            raise
