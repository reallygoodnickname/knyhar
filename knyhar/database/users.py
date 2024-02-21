# Subclass used for functions related to users
from sqlalchemy.orm import Session

from knyhar.models.users import User
from knyhar.database import SubclassTemplate


class UsersDatabase(SubclassTemplate):
    def __init__(self, database_obj):
        super().__init__(database_obj, User)

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
