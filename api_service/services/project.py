from sqlmodel import Session
from models.project import Project, ProjectCreate, ProjectUpdate, UserProject
from repositories.project import ProjectRepository, UserProjectRepository
from services.user import UserService


class ProjectService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = ProjectRepository(session=session)
        self.model = Project
    
    def create_project(self, project: ProjectCreate):
        project_db = self.model(
            name=project.name,
            description=project.description,
            status=project.status,
            begin_date=project.begin_date,
            end_date=project.end_date
        )
        return self.repo.create(object=project_db)
    
    def get_project_by_id(self, id: int):
        return self.repo.get_by_id(id=id)
    
    def get_projects(self):
        return self.repo.get_all()
    
    def update_project(self, id: int, project_update: ProjectUpdate):
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
    
    def delete_project(self, id: int):
        project = self.repo.get_by_id(id=id)
        if not project:
            return None
        is_deleted = self.repo.delete(object=project)
        if is_deleted:
            return True
        return False
    

class UserProjectService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = UserProjectRepository(session=session)
        self.model = UserProject
        self.project_service = ProjectService(session=session)
        self.user_service = UserService(session=session)
    
    def add_user_to_project(self, user_id: int, project_id: int):
        user = self.user_service.get_user_by_id(id=user_id)
        if not user:
            return None
        project = self.project_service.get_project_by_id(id=project_id)
        if not project:
            return None
        
        existing_user_project = self.repo.get_by_composite_id(user_id, project_id)
        if existing_user_project:
            return None
        
        user_project = self.model(user_id=user_id, project_id=project_id)
        return self.repo.create(object=user_project)

    def remove_user_from_project(self, user_id: int, project_id: int):
        user = self.user_service.get_user_by_id(id=user_id)
        if not user:
            return None
        
        project = self.project_service.get_project_by_id(id=project_id)
        if not project:
            return None
        
        existing_user_project = self.repo.get_by_composite_id(user_id, project_id)
        if not existing_user_project:
            return None
    
        is_deleted = self.repo.delete(object=existing_user_project)
        if is_deleted:
            return True
        return False