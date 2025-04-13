from sqlmodel import Session

from models.user import User, UserCreate, UserUpdate
from repositories.user import UserRepository


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = UserRepository(session=session)
        self.model = User

    def create_user(self, user: UserCreate):
        user_db = self.model(
            name=user.name,
            position=user.position,
            role_id=user.role_id,
        )
        return self.repo.create(object=user_db)

    def get_user_by_id(self, id: int):
        return self.repo.get_by_id(id=id)
    
    def get_users(self):
        return self.repo.get_all()
    
    def update_user(self, id: int, user_update: UserUpdate):
        user = self.repo.get_by_id(id=id)
        if not user:
            return None
        update_data = user_update.model_dump(exclude_unset=True)
        if not update_data:
            return None
        for field, value in update_data.items():
            setattr(user, field, value)

        updated_user = self.repo.update(object=user)
        
        if not updated_user:
            return None
        
        return self._transform_to_public(updated_user)
    
    def delete_user(self, id: int):
        user = self.repo.get_by_id(id=id)
        if not user:
            return None
        is_deleted = self.repo.delete(object=user)
        if is_deleted:
            return True
        return False