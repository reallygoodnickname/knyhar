from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class SubclassTemplate():
    def __init__(self, database_obj, model):
        self.database_obj = database_obj
        self.engine = database_obj.engine
        self.model = model

    def get_all(self):
        """
        Get all entities

        Arguments:
            None: This function doesn't take any arguments
        Returns:
            entity: List containing all entities
        """
        with Session(self.engine) as session:
            entities = session.query(self.model).all()

            return entities

    def get(self, id: int):
        """
        Get entity

        Arguments:
            id: Object id
        Returns:
            obj: Object or None, if not in database
        """
        with Session(self.engine) as session:
            obj = session.get(self.model, id)

            return obj

    def add(self, entity) -> bool:
        """
        Add entity

        Arguments:
            entity: Entity object to add
        Returns:
            bool: True  - added successfully
                  False - entity already exists
        """
        with Session(self.engine) as session:
            try:
                session.add(entity)
                session.commit()
            except IntegrityError:
                return False

            return True

    def remove(self, id: int) -> bool:
        """
        Remove entity

        Arguments:
            id: Entity ID
        Returns:
            bool: True  - removed successfully
                  False - entity doesn't exist
        """
        with Session(self.engine) as session:
            entity = self.get(id)

            if entity is None:
                return False

            session.delete(entity)
            session.commit()

            return True

    def add_relationship(self, target_obj, src_obj, relationship: str) -> bool:
        """
        Add relationship entity to a list
        """
        with Session(self.engine) as session:
            if None not in [target_obj, src_obj]:
                getattr(target_obj, relationship).append(src_obj)
                session.commit()

            return False

        return False
