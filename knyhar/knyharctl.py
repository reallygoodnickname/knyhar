import argparse

from sqlalchemy.orm import Session

from knyhar.settings import Settings
from knyhar.database.database import Database

options = [
    "promote",
    "demote",
    "get_user"
]


def switch(option: str):
    _switch = {
        "promote": promote_user,
        "demote": demote_user,
        "get_user": get_user
    }
    return _switch[option]


def promote_user(database: Database, id: int):
    res = database.users.set_role(id, True)

    if res:
        print("Promoted user successfully!")
    else:
        print("Wrong user ID!")


def demote_user(database: Database, id: int):
    res = database.users.set_role(id, False)

    if res:
        print("Demoted user successfully!")
    else:
        print("Wrong user ID!")


def get_user(database: Database, id: int):
    user = database.users.get(id)

    if user is not None:
        with Session(database.engine) as session:
            print(user.get_pydantic_model(session))
    else:
        print("User not found!")


def main(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    settings = Settings()

    database = Database(host=settings.host,
                        username=settings.db_username,
                        password=settings.db_password)

    func = switch(args.command)
    func(database, args.id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='knyharctl',
                                     description='Online library demo')

    parser.add_argument('command', choices=options, help="Action to perform")
    parser.add_argument('id', help="Identifier of the entity", type=int)

    main(parser)
