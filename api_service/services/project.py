from sqlmodel import Session
from typing import List

from models.project import Project, ProjectCreate, ProjectUpdate, UserProject
from repositories.project import ProjectRepository, UserProjectRepository
from services.user import UserService


class ProjectService:
    def __init__(self, session: Session):
        """
        Initializes the ProjectService with the given database session.

        Args:
            session (Session): The database session for interacting with the
            database.
        """
        self.session = session
        self.repo = ProjectRepository(session=session)
        self.model = Project
    
    def create_project(self, project: ProjectCreate) -> Project | None:
        """
        Creates a new project in the database.

        Args:
            project (ProjectCreate): The project data to create, provided as a
            SQLmodel instance.

        Returns:
            Project | None: The created project instance after saving it to the
            database, or None if an error occurs during creation.
        """
        project_db = self.model(
            name=project.name,
            description=project.description,
            status=project.status,
            begin_date=project.begin_date,
            end_date=project.end_date
        )
        return self.repo.create(object=project_db)
    
    def get_project_by_id(self, id: int) -> Project | None:
        """
        Retrieves a project by its ID.

        Args:
            id (int): The ID of the project to retrieve.

        Returns:
            Project | None: The project instance with the specified ID, or None
            if not found.
        """
        return self.repo.get_by_id(id=id)
    
    def get_projects(self) -> List[Project]:
        """
        Retrieves all projects from the database.

        Returns:
            List[Project]: A list of all project instances in the database.
        """
        return self.repo.get_all()
    
    def update_project(
        self,
        id: int,
        project_update: ProjectUpdate
    ) -> Project | None:
        """
        Updates an existing project by its ID.

        Args:
            id (int): The ID of the project to update.
            project_update (ProjectUpdate): The data to update the project
            with, provided as a SQLModel model.

        Returns:
            Project | None: The updated project instance, or None if not found
            or unable to update.
        """
        project = self.repo.get_by_id(id=id)
        if not project:
            return None
        update_data = project_update.model_dump(exclude_unset=True)
        if not update_data:
            return None
        for field, value in update_data.items():
            setattr(project, field, value)

        updated_project = self.repo.update(object=project)
        
        if not updated_project:
            return None
        
        return self._transform_to_public(updated_project)
    
    def delete_project(self, id: int) -> bool | None:
        """
        Deletes a project by its ID.

        Args:
            id (int): The ID of the project to delete.

        Returns:
            bool | None: True if the project was successfully deleted, False if
            an error occurred during deletion, or None if the project was not
            found.
        """
        project = self.repo.get_by_id(id=id)
        if not project:
            return None
        is_deleted = self.repo.delete(object=project)
        if is_deleted:
            return True
        return False
    

class UserProjectService:
    def __init__(self, session: Session) -> UserProject | None:
        """
        Initializes the UserProjectService with the given database session.

        Args:
            session (Session): The database session for interacting with the
            database.
        """
        self.session = session
        self.repo = UserProjectRepository(session=session)
        self.model = UserProject
        self.project_service = ProjectService(session=session)
        self.user_service = UserService(session=session)
    
    def add_user_to_project(self, user_id: int, project_id: int):
        """
        Adds a user to a project.

        Args:
            user_id (int): The ID of the user to add.
            project_id (int): The ID of the project to add the user to.

        Returns:
            UserProject: The created UserProject instance, or None if the user
            is already added or not found.
        """
        user = self.user_service.get_user_by_id(id=user_id)
        if not user:
            return None
        project = self.project_service.get_project_by_id(id=project_id)
        if not project:
            return None
        
        existing_user_project = self.repo.get_by_composite_id(
            user_id, project_id
        )
        if existing_user_project:
            return None
        
        user_project = self.model(user_id=user_id, project_id=project_id)
        return self.repo.create(object=user_project)

    def remove_user_from_project(
        self,
        user_id: int, 
        project_id: int
    ) -> bool | None:
        """
        Removes a user from a project.

        Args:
            user_id (int): The ID of the user to remove.
            project_id (int): The ID of the project to remove the user from.

        Returns:
            bool | None: True if the user was successfully removed, False if an
            error occurred during removal, or None if the user, project, or
            the association between them was not found.
        """
        user = self.user_service.get_user_by_id(id=user_id)
        if not user:
            return None
        
        project = self.project_service.get_project_by_id(id=project_id)
        if not project:
            return None
        
        existing_user_project = self.repo.get_by_composite_id(
            user_id, project_id
        )
        if not existing_user_project:
            return None
    
        is_deleted = self.repo.delete(object=existing_user_project)
        if is_deleted:
            return True
        return False