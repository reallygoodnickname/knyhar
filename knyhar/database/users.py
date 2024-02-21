# Subclass used for functions related to users
from sqlalchemy.orm import Session

from sqlalchemy import delete, select, update
import sqlalchemy.exc

from knyhar.models.users import User


class UsersDatabase():
    def __init__(self, parent_obj):
        self.parent_obj = parent_obj
        self.engine = parent_obj.engine

    def get(self, id: int) -> User | None:
        """
        Get user by id

        Arguments:
            id: User's id 
        Returns:
            User | None: This function will return User
                         object or None if user doesn't exist
        """
        with Session(self.engine) as session:
            user = session.get(User, id)

            return user

    def set_role(self, id: int, role: bool) -> bool:
        """
        Grant or invoke user permissions 

        Arguments:
            id: Target user id
            role: Desired user role
                  True  - admin
                  False - regular
        Returns:
            bool: True  - updated user's role 
                  False - user doesn't exist
        """
        with Session(self.engine) as session:
            user = self.get(id)

            if user is None:
                return False

            user.admin = role
            session.add(user)
            session.commit()

            return True

    def add(self, user: User) -> bool:
        """
        Add user

        Arguments:
            user: User object
        Returns:
            bool: True  - added successfully 
                  False - user already exists 
        """
        with Session(self.engine) as session:
            try:
                session.add(user)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                return False

            return True

    def remove(self, id: int) -> bool:
        """
        Remove user

        Arguments:
            id: User id
        Returns:
            bool: True  - removed successfully
                  False - user doesn't exist
        """
        with Session(self.engine) as session:
            user = self.get(id)

            if user is None:
                return False

            session.delete(user)
            session.commit()

            return True

    def remove_favorite(self):
        """ Remove book from favorites """
        pass

    def add_favorite(self):
        """ Add book to favorites """
        pass
