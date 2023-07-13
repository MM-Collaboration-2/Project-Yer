from object import Object


class Integer(Object):
    regex = '[-]?\d+'
    type: str = 'integer'
    def __init__(self, number):
        self.data = int(number)

    def __repr__(self):
        return str(self.data)
