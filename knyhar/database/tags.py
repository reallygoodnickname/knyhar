from knyhar.models.tags import Tag
from knyhar.database import SubclassTemplate


class TagsDatabase(SubclassTemplate):
    def __init__(self, database_obj):
        super().__init__(database_obj, Tag)
