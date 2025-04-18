from repositories.base import BaseRepository
from models.role import Role


class RoleRepository(BaseRepository):
    def __init__(self, session):
        """
        Initializes the role repository.

        Args:
            session: The database session (sqlmodel.Session).
        """
        super().__init__(model=Role, session=session)