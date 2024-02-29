class Entity(Exception):
    def __init__(self, entity=None):
        self.entity = entity


class EntityNotFound(Entity):
    pass


class EntityAlreadyAdded(Entity):
    pass


class EntityMissing(Entity):
    pass


class EntityExists(Entity):
    pass
