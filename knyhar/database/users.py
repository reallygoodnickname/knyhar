# Subclass used for functions related to users
from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session

from knyhar.models.users import User
from knyhar.database import SubclassTemplate


class UsersDatabase(SubclassTemplate):
    def __init__(self, database_obj):
        super().__init__(database_obj, User)

    def get_user_by_username(self, username: str) -> User | None:
        """
        Get user password by username

        Arguments:
            username: Username to look for
        Returns:
            User | None: This function will either return found user,
                         or None, if user is not found
        """
        with Session(self.engine) as session:
            user = select(User).where(User.username == username)

            res = session.execute(user).first()

            if res is not None:
                return res[0]

            return None

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

    def add_favorite(self, user_id: int, book_id: int) -> None:
        """
        Add favorite book by id

        Arguments:
            user_id: User ID
            book_id: Book ID
        Returns:
            None: This function doesn't return anything
        """
        return self.add_entity(user_id, book_id, "books", "favorites")

    def remove_favorite(self, user_id: int, book_id: int) -> None:
        """
        Remove favorite book by id

        Arguments:
            user_id : User ID
            book_id: Book ID
        Returns:
            None: This function doesn't return anything
        """

        return self.remove_entity(user_id, book_id, "books", "favorites")
