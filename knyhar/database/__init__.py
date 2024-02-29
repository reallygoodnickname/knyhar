from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from knyhar.database.exc import (EntityNotFound,
                                 EntityAlreadyAdded,
                                 EntityMissing)


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

    def add_entity(self, src_id: int, dest_id: int,
                   src_table: str, relationship: str) -> None:
        """
        Add entity to a relationship list of another entity

        Arguments:
            src_id: Object's ID to what entity should be added 
            src_id: Object's ID that should be added 
            src_table: Source's table from which added object should be taken
            relationship: Relationship field string 
        Returns:
            None: This function doesn't return anything
        """
        with Session(self.engine) as session:
            dest_entity = self.get(dest_id)
            src_entity = getattr(self.database_obj, src_table).get(src_id)
            if None not in [dest_entity, src_entity]:
                session.add(dest_entity)

                try:
                    getattr(dest_entity, relationship).append(src_entity)
                    session.commit()
                except InvalidRequestError:
                    raise EntityAlreadyAdded

            else:
                raise EntityNotFound(src_id)

    def remove_entity(self, dest_id: int, src_id: int,
                      src_table: str, relationship: str) -> None:
        """
        Remove entity from a relationship list of another entity

        Arguments:
            dest_id: Object's ID from what entity should be removed
            src_id: Object's ID that should be removed
            src_table: Source's table
            relationship: Relationship field string 
        Returns:
            None: This function doesn't return anything
        """
        with Session(self.engine) as session:
            dest_entity = self.get(dest_id)
            src_entity = getattr(self.database_obj, src_table).get(src_id)
            if None not in [dest_entity, src_entity]:
                session.add_all([dest_entity, src_entity])

                try:
                    getattr(dest_entity, relationship).remove(src_entity)
                    session.commit()
                except ValueError:
                    raise EntityMissing

            else:
                raise EntityNotFound(src_id)
