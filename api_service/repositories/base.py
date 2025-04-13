from sqlmodel import SQLModel, Session, select


class BaseRepository:
    def __init__(self, model, session: Session):
        """
        Clase base para repositorios con implementaciones CRUD genéricas.

        :param model: La clase del modelo SQLModel que manejará este repositorio
                      (ej: User, Item).
        :param session: La sesión de base de datos (sqlmodel.Session).
        """
        if not issubclass(model, SQLModel):
             raise TypeError(f"El parámetro 'model' debe ser una subclase de SQLModel, se recibió {type(model)}")
        self._model = model
        self.session = session

    def get_by_id(self, id: int):
        """
        Obtiene un único registro por su ID.

        :param id: El identificador del registro a buscar.
        :return: Una instancia del modelo encontrado o None si no existe.
        """
        return self.session.get(self._model, id)
    
    def get_by_composite_id(self, *ids):
        return self.session.get(self._model, ids)

    def get_all(self):
        """
        Obtiene una lista de registros, con opción de paginación.

        :return: Una lista de instancias del modelo.
        """
        statement = select(self._model)
        results = self.session.exec(statement)
        return results.all()

    def create(self, object):
        """
        Crea un nuevo registro en la base de datos.

        :param object: Un objeto (normalmente un schema Pydantic/SQLModel como UserCreate)
                       con los datos para crear el nuevo registro.
                       Se espera que sea compatible para crear una instancia de self._model.
        :return: La instancia del modelo recién creada y refrescada desde la BD.
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
        Actualiza un registro existente por su ID.

        :param object: Un objeto (normalmente un schema Pydantic/SQLModel como UserUpdate)
                       con los datos a actualizar. Solo los campos presentes se actualizarán.
        :return: La instancia del modelo actualizada o None si no se encontró el registro.
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
        Elimina un registro de la base de datos por su ID.

        :param object: Un objeto a eliminar
        :return: La instancia del modelo eliminado (ahora detached de la sesión) o None si no se encontró.
        """
        try:
            self.session.delete(object)
            self.session.commit()
            return True
        except Exception as e:
            return False