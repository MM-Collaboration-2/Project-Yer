from object import Object


class Float(Object):
    regex = '-?\d+\.\d+'
    type: str = 'float'
    def __init__(self, number):
        self.data = float(number)

    def __repr__(self):
        return str(self.data)
