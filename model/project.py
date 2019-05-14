class Project:

    def __init__(self, id=None, name=None, description=None):  # если задать '', то поле будет очищаться
        self.id = id
        self.name = name
        self.description = description

    def __repr__(self):
        return '{%s:%s}' % (self.id, self.name)
