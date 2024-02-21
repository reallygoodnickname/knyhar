import sqlalchemy
from sqlalchemy.orm import Session
from knyhar.models.tags import Tag


class TagsDatabase():
    def __init__(self, parent_obj):
        self.parent_obj = parent_obj
        self.engine = parent_obj.engine

    def get(self, id: int) -> Tag | None:
        """
        Get tag by id

        Arguments:
            id: Tag's id
        Returns:
            Tag | None: This function will return either tag or None 
        """
        with Session(self.engine) as session:
            tag = session.get(Tag, id)

            return tag

    def add(self, tag: Tag) -> bool:
        """
        Add tag

        Arguments:
            tag: Tag to add 
        Returns:
            bool: True - added successfully
                  False - tag already exists
        """
        with Session(self.engine) as session:
            try:
                session.add(tag)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                return False

            return True

    def remove(self, id: int) -> bool:
        """
        Remove tag

        Arguments:
            id: Tag id
        Returns:
            bool: True - remove successfully
                  False - tag doesn't exist
        """
        with Session(self.engine) as session:
            tag = self.get(id)

            if tag is None:
                return False

            session.delete(tag)
            session.commit()

            return True
