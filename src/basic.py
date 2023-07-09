class Object():                         # базовый класс для всех типов
    def __init__(self, data=0):
        self.type: str = 'object'
        self.data: int = 0              # как и в С. данные можно хранить 
                                        # исплоьзуя лишь число
    def __str__(self):
        return str(self.data)


class Variable(Object):                 # Переменная. Может хранить число
    def __init__(self, name, data=0):   
        self.type = 'variable'          
        self.name: str = name           
        self.data: int = data

    def __str__(self):
        return str(self.data)


class Int(Object):                      # Основной тип данных
    def __init__(self, number):          
        self.type = "int"               
        self.data = int(number)         

    @classmethod
    def from_string(cls, string: str):  # Нет парсера строки в число
        number: int = int(string)       # надеемся что конвертнется
        return Int(number)


class Stack():                          # Стек для дерева выражений
    def __init__(self):                 # костыль, надстройка над list'ом
        self.list = list()

    def is_empty(self):
        return len(self.list) == 0

    def pop(self):
        return self.list.pop()

    def peek(self):
        return self.list[-1]

    def push(self, data):
        self.list.append(data)

    def __str__(self):
        str(self.list)

