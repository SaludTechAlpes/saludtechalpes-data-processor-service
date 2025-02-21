from uuid import UUID
from sqlalchemy.orm import Session
from modulos.anonimizacion.dominio.repositorios import RepositorioImagenAnonimizada
from modulos.anonimizacion.dominio.entidades import ImagenAnonimizada
from modulos.anonimizacion.infraestructura.dto import ImagenAnonimizadaDTO
from modulos.anonimizacion.infraestructura.mapeadores import MapeadorImagenAnonimizada
from modulos.anonimizacion.infraestructura.db import db

class RepositorioImagenAnonimizadaPostgres(RepositorioImagenAnonimizada):
    def __init__(self, session: Session):
        self.session = session
        self.mapeador = MapeadorImagenAnonimizada()

    def obtener_por_id(self, id: UUID) -> ImagenAnonimizada:
        imagen_dto = self.session.query(ImagenAnonimizadaDTO).filter_by(id=str(id)).one_or_none()
        if not imagen_dto:
            return None
        return self.mapeador.dto_a_entidad(imagen_dto)

    def obtener_todos(self) -> list[ImagenAnonimizada]:
        imagenes_dto = self.session.query(ImagenAnonimizadaDTO).all()
        return [self.mapeador.dto_a_entidad(imagen_dto) for imagen_dto in imagenes_dto]

    def agregar(self, imagen: ImagenAnonimizada):
        imagen_dto = self.mapeador.entidad_a_dto(imagen)
        self.session.add(imagen_dto)
        self.session.commit()

    def actualizar(self, imagen: ImagenAnonimizada):
        imagen_dto = self.mapeador.entidad_a_dto(imagen)
        self.session.merge(imagen_dto)
        self.session.commit()

    def eliminar(self, id: UUID):
        self.session.query(ImagenAnonimizadaDTO).filter_by(id=str(id)).delete()
        self.session.commit()
