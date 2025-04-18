from sqlmodel import Session
from typing import List

from models.user import User, UserCreate, UserUpdate
from repositories.user import UserRepository


class UserService:
    def __init__(self, session: Session) -> None:
        """
        Initializes the UserService with the given database session.

        Args:
            session (Session): The database session for interacting with the
            database.
        """
        self.session = session
        self.repo = UserRepository(session=session)
        self.model = User

    def create_user(self, user: UserCreate) -> User | None:
        """
        Creates a new user in the database.

        Args:
            user (UserCreate): A SQLModel instance containing the user data to
            be created.

        Returns:
            User | None: The created User instance after saving it to the
            database, or None if an error occurs during creation.
        """
        user_db = self.model(
            name=user.name,
            position=user.position,
            role_id=user.role_id,
        )
        return self.repo.create(object=user_db)

    def get_user_by_id(self, id: int) -> User | None:
        """
        Retrieves a user by their ID.

        Args:
            id (int): The ID of the user to retrieve.

        Returns:
            User | None: The User instance if found, otherwise None.
        """
        return self.repo.get_by_id(id=id)
    
    def get_users(self) -> List[User]:
        """
        Retrieves all users from the database.

        Returns:
            List[User]: A list of all user instances in the database.
        """
        return self.repo.get_all()
    
    def update_user(self, id: int, user_update: UserUpdate) -> User | None:
        """
        Updates an existing user by their ID.

        Args:
            id (int): The ID of the user to update.
            user_update (UserUpdate): The data to update the user with,
            provided as a SQLModel model.

        Returns:
            User | None: The updated user instance, or None if the user was not
            found or an error occurred during the update.
        """
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
    
    def delete_user(self, id: int) -> bool | None:
        """
        Deletes a user by their ID.

        Args:
            id (int): The ID of the user to delete.

        Returns:
            bool | None: True if the user was successfully deleted, False if
            an error occurred during deletion, or None if the user was not
            found.
        """
        user = self.repo.get_by_id(id=id)
        if not user:
            return None
        is_deleted = self.repo.delete(object=user)
        if is_deleted:
            return True
        return False