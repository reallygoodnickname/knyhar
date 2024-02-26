import unittest

from sqlalchemy.types import (Integer,
                              String)
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session,
                            mapped_column)

from knyhar.database import SubclassTemplate
from tests.mocks.database import database


class Base(DeclarativeBase):
    pass


class Entity(Base):
    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)

    def __repr__(self):
        return f'Entity(id={self.id}, name={self.name})'


class TestSubclassTemplate(unittest.TestCase):
    def setUp(self):
        self.database = database.MockDatabase()
        self.model = Entity
        self.entity_count = 4
        self.template = SubclassTemplate(self.database, self.model)

        # Create database from separate declarative base
        Base.metadata.tables['entity'].create(self.database.engine)

        # Populate database with test data
        with Session(self.database.engine) as session:
            for i in range(1, 5):
                session.add(Entity(id=i, name=f"Entity{i}"))

            session.commit()

    def test_get_exists(self):
        """ Get entity from database with correct id """
        res = self.template.get(1)

        self.assertIsInstance(res, self.model)

    def test_get_not_exists(self):
        """ Get entity from database with incorrect id """
        res = self.template.get(-1)

        self.assertIsNone(res)

    def test_add_exists(self):
        """ Add entity that exists """
        entity = Entity(id=1, name=f"Entity1")

        self.assertFalse(self.template.add(entity))

    def test_add_not_exists(self):
        """ Add entity that doesn't exist """
        entity = Entity(id=6, name=f"Entity6")

        self.entity_count += 1

        self.assertTrue(self.template.add(entity))

    def test_remove_exists(self):
        """ Remove entity that exists """
        res = self.template.remove(1)
        self.entity_count -= 1

        self.assertTrue(res)

    def test_remove_doesnt_exist(self):
        """ Remove entity that doesn't exist """
        res = self.template.remove(-1)

        self.assertFalse(res)

    def test_get_all_entities(self):
        """ Get all entities from database """
        res = self.template.get_all()

        self.assertEqual(len(res), self.entity_count)
