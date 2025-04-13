from sqlmodel import Session

from models.role import Role, RoleCreate, RoleUpdate
from repositories.role import RoleRepository


class RoleService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = RoleRepository(session=session)
        self.model = Role
    
    def create_role(self, role: RoleCreate):
        role_db = self.model(
            name=role.name,
            description=role.description
        )
        return self.repo.create(object=role_db)
    
    def get_role_by_id(self, id: int):
        return self.repo.get_by_id(id=id)
    
    def get_roles(self):
        return self.repo.get_all()
    
    def update_role(self, id: int, role_update: RoleUpdate):
        role = self.repo.get_by_id(id=id)
        if not role:
            return None
        update_data = role_update.model_dump(exclude_unset=True)
        if not update_data:
            return None
        for field, value in update_data.items():
            setattr(role, field, value)

        updated_role = self.repo.update(object=role)
        
        if not updated_role:
            return None
        
        return self._transform_to_public(updated_role)
    
    def delete_role(self, id: int):
        role = self.repo.get_by_id(id=id)
        if not role:
            return None
        if role.users:
            return None
        is_deleted = self.repo.delete(object=role)
        if is_deleted:
            return True
        return False