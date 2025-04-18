from repositories.base import BaseRepository
from models.user import User


class UserRepository(BaseRepository):
    def __init__(self, session):
        """
        Initializes the user repository.

        Args:
            session: The database session (sqlmodel.Session).
        """
        super().__init__(model=User, session=session)