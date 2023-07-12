## Yer basic objects
from utils import tokens, token_type

class Object():
    regex = '.*?'
    type: str = 'object'
    def __init__(self, data=0):
        self.data: int = data
                                        
    def __repr__(self):
        return f'o#' + str(self.data)


class Integer(Object):
    regex = '[-]?\d+'
    type: str = 'integer'
    def __init__(self, number):
        self.data = int(number)

    def __repr__(self):
        return f'i#' + str(self.data)


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

    def __repr__(self):
        return f's#' + '"' + str(self.data) + '"'




class Float(Object):
    regex = '-?\d+\.\d+'
    type: str = 'float'
    def __init__(self, number):
        self.data = float(number)

    def __repr__(self):
        return f'f#' + str(self.data)




class List(Object):
    regex = '\[.*\]'
    type: str = 'list'

    def __init__(self, objects: str):
        self.objects: str = objects
        self.data = self.validate()

    def validate(self) -> list[Object]:
        lst = []
        objects = tokens(self.objects[1:-1])
        for obj in objects:
            obj_type = token_type(obj)
            lst.append(BASIC_TYPES[obj_type](obj))
        
        return lst
    
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
        return 'l#' + str(self.data)



class Variable(Object):                     # Хранит объект
    regex = '[\u263a-\U0001f645а-яА-Яa-zA-Z][\u263a-\U0001f645а-яА-Яa-zA-Z0-9_]*'
    type: str = 'variable'
    def __init__(self, name, obj: Object = Object()):   
        self.name: str = name           
        self.obj: Object = obj

    def __repr__(self):
        return f'v#{self.name}=' + str(self.obj)



global BASIC_OBJECTS
BASIC_OBJECTS: list[Object] = [Integer, Float, String, List, Variable]
global BASIC_TYPES
BASIC_TYPES: dict[str: Object] = {obj.type: obj for obj in BASIC_OBJECTS}



if __name__ == '__main__':
    l = List('[a,-2,0.43,]')
    v = Variable('lst', l)
    print(v)

