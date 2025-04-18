from sqlmodel import Session
from typing import List

from models.role import Role, RoleCreate, RoleUpdate
from repositories.role import RoleRepository


class RoleService:
    def __init__(self, session: Session) -> None:
        """
        Initializes the RoleService with the given database session.

        Args:
            session (Session): The database session for interacting with the
            database.
        """
        self.session = session
        self.repo = RoleRepository(session=session)
        self.model = Role
    
    def create_role(self, role: RoleCreate) -> Role | None:
        """
        Creates a new role in the database.

        Args:
            role (RoleCreate): A SQLModel instance containing the role data
            to be created.

        Returns:
            Role | None: The created Role instance after saving it to the
            database, or None if an error occurs during creation.
        """
        role_db = self.model(
            name=role.name,
            description=role.description
        )
        return self.repo.create(object=role_db)
    
    def get_role_by_id(self, id: int) -> Role | None:
        """
        Retrieves a role by its ID.

        Args:
            id (int): The ID of the role to retrieve.

        Returns:
            Role | None: The Role instance if found, otherwise None.
        """
        return self.repo.get_by_id(id=id)
    
    def get_roles(self) -> List[Role]:
        """
        Retrieves all roles from the database.

        Returns:
            List[Role]: A list of all role instances in the database.
        """
        return self.repo.get_all()
    
    def update_role(self, id: int, role_update: RoleUpdate) -> Role | None:
        """
        Updates an existing role by its ID.

        Args:
            id (int): The ID of the role to update.
            role_update (RoleUpdate): The data to update the role with,
            provided as a SQLModel model.

        Returns:
            Role | None: The updated role instance, or None if the role was not
            found or an error occurred during the update.
        """
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
    
    def delete_role(self, id: int)  -> bool | None:
        """
        Deletes a role by its ID, only if it's not assigned to any user.

        Args:
            id (int): The ID of the role to delete.

        Returns:
            bool | None: True if the role was successfully deleted, False if an
            error occurred during deletion, or None if the role was not found
            or is currently assigned to users.
        """
        role = self.repo.get_by_id(id=id)
        if not role:
            return None
        if role.users:
            return None
        is_deleted = self.repo.delete(object=role)
        if is_deleted:
            return True
        return False