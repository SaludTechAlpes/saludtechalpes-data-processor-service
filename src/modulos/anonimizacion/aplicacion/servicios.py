from datetime import datetime, timezone
import uuid
from modulos.anonimizacion.dominio.reglas import FormatoImagenValido
from modulos.anonimizacion.dominio.eventos import ImagenAnonimizadaEvento
from modulos.anonimizacion.dominio.entidades import ImagenAnonimizada, MetadatosAnonimizados
from seedwork.aplicacion.servicios import Servicio
from modulos.anonimizacion.infraestructura.adaptadores import AdaptadorAnonimizacion
from modulos.anonimizacion.dominio.repositorios import RepositorioImagenAnonimizada

class ServicioAplicacionAnonimizacion(Servicio):
    """Orquesta la anonimización de imágenes y metadatos."""

    def __init__(self, adaptador_anonimizacion: AdaptadorAnonimizacion, repositorio_imagenes: RepositorioImagenAnonimizada):
        self.adaptador_anonimizacion = adaptador_anonimizacion
        self.repositorio_imagenes = repositorio_imagenes

    def anonimizar_imagen(self, id_imagen: uuid.UUID, ruta_imagen: str, ruta_archivo_metadatos: str):
        """Orquesta la validación, ejecución de anonimización y publicación del evento."""

        self.validar_regla(FormatoImagenValido(ruta_imagen))

        datos_anonimizados = self.adaptador_anonimizacion.anonimizar(ruta_imagen, ruta_archivo_metadatos)

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
            estado="PROCESADO",
            metadatos=metadatos_anonimizados
        )

        self.repositorio_imagenes.agregar(imagen_anonimizada)

        evento = ImagenAnonimizadaEvento(
            id_imagen=id_imagen,
            ruta_imagen_anonimizada=imagen_anonimizada.ruta_imagen_anonimizada,
            fecha=datetime.now(timezone.utc)
        )

        self.publicar_evento(evento)
