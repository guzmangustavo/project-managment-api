from repositories.base import BaseRepository
from models.project import Project, UserProject


class ProjectRepository(BaseRepository):
    def __init__(self, session):
        """
        Initializes the project repository.

        :param session: The database session (sqlmodel.Session).
        """
        super().__init__(model=Project, session=session)


class UserProjectRepository(BaseRepository):
    def __init__(self, session):
        """
        Initializes the user project repository.

        :param session: The database session (sqlmodel.Session).
        """
        super().__init__(model=UserProject, session=session)