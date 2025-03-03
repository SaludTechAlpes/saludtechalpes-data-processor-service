from uuid import UUID
from src.modulos.mapeo.dominio.puertos.repositorios import RepositorioImagenMapeada
from src.modulos.mapeo.dominio.entidades import ImagenMapeada
from src.modulos.mapeo.infraestructura.dto import ImagenMapeadaDTO
from src.modulos.mapeo.infraestructura.mapeadores import MapeadorImagenMapeada
from src.config.db import get_db

class RepositorioImagenMapeadaPostgres(RepositorioImagenMapeada):
    def __init__(self):
        self.session = next(get_db())
        self.mapeador = MapeadorImagenMapeada()

    def obtener_por_id(self, id: UUID) -> ImagenMapeada:
        imagen_dto = self.session.query(ImagenMapeadaDTO).filter_by(id=str(id)).one_or_none()
        return self.mapeador.dto_a_entidad(imagen_dto)


    def obtener_todos(self) -> list[ImagenMapeada]:
        imagenes_dto = self.session.query(ImagenMapeadaDTO).all()
        return [self.mapeador.dto_a_entidad(imagen_dto) for imagen_dto in imagenes_dto]

    def agregar(self, imagen: ImagenMapeada):
        imagen_dto = self.mapeador.entidad_a_dto(imagen)

        self.session.add(imagen_dto)
        self.session.commit()

    def actualizar(self, imagen: ImagenMapeada):
        imagen_dto = self.mapeador.entidad_a_dto(imagen)
        self.session.merge(imagen_dto)
        self.session.commit()

    def eliminar(self, id: UUID):
        self.session.query(ImagenMapeadaDTO).filter_by(id=str(id)).delete()
        self.session.commit()
