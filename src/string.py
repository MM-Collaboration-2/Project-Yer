from object import Object


class String(Object):
    regex = '\".*?\"'
    type: str = 'string'
    def __init__(self, string):
        self.data = str(string)
        self.validate()

    def validate(self):
        if self.data.startswith('"'):
            self.data = self.data[1:]
        if self.data.endswith('"'):
            self.data = self.data[:-1]

    def len(self) -> int:
        return len(self.data)


    def get(self, index: int) -> Object:
        return String(self.data[index])


    def __repr__(self):
        return '"' + self.data + '"'
