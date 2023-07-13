from object import Object


class List(Object):
    regex = '\[.*\]'
    type: str = 'list'

    def __init__(self, data: list[Object]):
        self.data = data

    def copy(self):
        l = List(self.objects)
        return l

    def add(self, obj: Object):
        self.data.append(obj)

    def remove(self, index: int):
        self.data.remove[index]

    def len(self) -> int:
        return len(self.data)

    def get(self, index: int) -> Object:
        return self.data[index]

    def __repr__(self):
        return str(self.data)

