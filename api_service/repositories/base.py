from sqlmodel import SQLModel, Session, select


class BaseRepository:
    def __init__(self, model, session: Session):
        """
        Base class for repositories with generic CRUD implementations.

        Args:
            model: The SQLModel class that this repository will manage
                   (e.g., User, Project).
            session: The database session (sqlmodel.Session).
        """
        if not issubclass(model, SQLModel):
             raise TypeError(
                f"The 'model' parameter must be a subclass of SQLModel, "
                f"received {type(model)}"
            )
        self._model = model
        self.session = session

    def get_by_id(self, id: int):
        """
        Retrieves a single record by its ID.

        Args:
            id: The identifier of the record to search for.

        Returns:
            An instance of the model if found, or None if it doesn't exist.
        """
        return self.session.get(self._model, id)
    
    def get_by_composite_id(self, *ids):
        """
        Retrieves a record by its composite ID.

        Args:
            *ids: The individual composite key values to identify the record.

        Returns:
            The instance of the model if found, or None if it doesn't exist.
        """
        return self.session.get(self._model, ids)

    def get_all(self):
        """
        Retrieves a list of records.

        Returns:
            A list of model instances.
        """
        statement = select(self._model)
        results = self.session.exec(statement)
        return results.all()

    def create(self, object):
        """
        Creates a new record in the database.

        Args:
            object: An object (a SQLModel instance like ProjectCreate)
                    containing the data to create the new record.
                    It is expected to be compatible with the model.

        Returns:
            The newly created and refreshed model instance from the database or
            None if an error occurs during the process..
        """
        try:
            self.session.add(object)
            self.session.commit()
            self.session.refresh(object)
            return object
        except Exception as e:
            return None

    def update(self, object):
        """
        Updates an existing record with the provided data.

        Args:
            object: An object (a SQLModel instance like UserUpdate)
                    containing the data to update. Only the fields present will
                    be updated.

        Returns:
            The updated model instance if successful, or None if the record was
            not found or an error occurred.
        """
        try:
            self.session.add(object)
            self.session.commit()
            self.session.refresh(object)
            return object
        except Exception as e:
            return None
        

    def delete(self, object):
        """
        Deletes a record from the database.

        Args:
            object: The object to delete.

        Returns:
            True if the deletion was successful, or False if an error occurred
            or the record was not found.
        """
        try:
            self.session.delete(object)
            self.session.commit()
            return True
        except Exception as e:
            return False