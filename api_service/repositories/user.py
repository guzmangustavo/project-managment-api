from repositories.base import BaseRepository
from models.user import User


class UserRepository(BaseRepository):
    def __init__(self, session):
        """
        Inicializa el repositorio de usuarios.

        :param session: La sesión de base de datos (sqlmodel.Session).
        """
        super().__init__(model=User, session=session)