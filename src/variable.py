from object import Object


class Variable(Object):                     # Хранит объект
    regex = '[a-zA-Z][a-zA-Z0-9_]*'
    type: str = 'variable'
    def __init__(self, name, obj: Object = Object()):   
        self.name: str = name           
        self.obj: Object = obj

    def __repr__(self):
        return str(self.obj)
