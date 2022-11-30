import dataclasses


@dataclasses.dataclass
class ValidWords:
    id: int
    name: str
    status: int

    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def setId(self, id):
        self.id = id
