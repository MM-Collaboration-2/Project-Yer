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

    def __repr__(self):
        return str(self.list)


## Yer objects

class Object():                         # базовый класс для всех типов
    def __init__(self, data=0):
        self.type: str = 'object'
        self.data: int = data              # как и в С. данные можно хранить 
                                        # исплоьзуя лишь число
    def __repr__(self):
        return f'o#' + str(self.data)


class Integer(Object):                      # Основной тип данных
    def __init__(self, number):          
        self.type = 'integer'               
        self.data = int(number)         

    def __repr__(self):
        return f'i#' + str(self.data)

class String(Object):
    def __init__(self, string):
        self.type = 'string'
        self.data = str(string)

    def __repr__(self):
        return f's#' + str(self.data)


class Float(Object):
    def __init__(self, number):
        self.type = 'float'
        self.data = float(number)

    def __repr__(self):
        return f'f#' + str(self.data)


class Node(Object):
    def __init__(self, data: Object):
        self.type = 'list_node'
        self.data = data
        self.next = None

    def __repr__(self):
        return f'n#' + str(self.data)


class List(Object):
    def __init__(self, elements=None):
        self.type = 'list'
        self.start = None
        self.end = None
        self.data = None

        if elements:
            for element in elements:
                self.append(element)

    def __repr__(self):
        return 'l#[{}]'.format(', '.join(str(i) for i in self))

    def __len__(self):
        return self.length()

    def __iter__(self):
        node = self.start
        while node: 
            yield node
            node = node.next 
        
    def __add__(self, other):
        left_list = copy.deepcopy(self)
        right_list = copy.deepcopy(other)
        if not left_list.start:
            return right_list
        if not right_list.start:
            return left_list
        
        left_list.end.next = right_list.start 
        left_list.end = right_list.end 
        return left_list

    def __iadd__(self, other):
        self = self + other
        return self

    def __eq__(self, other):
        if self.length() != other.length():
            return False
        for i,j in zip(self, other):
            if i != j: 
                return False
        return True

    def append(self, data):
        node = Node(data)
        if not self.start: 
            self.start = node
        else: 
            self.end.next = node 
        self.end = node 
            
    def get(self, index):
        if not 0 <= index < self.length():
            raise IndexError
        for pos, node in enumerate(self):
            if pos == index:
                return node
 
    def length(self):
        return sum(1 for _ in self)
        
    def pop(self, index=None):
        list_length = self.length()
        if index == None: 
            index = list_length - 1 
        if not 0 <= index < list_length:
            raise IndexError
        node_to_remove = self[index] 
        if index == 0: 
            if list_length == 1: 
                self.start = None
                self.end = None
            else:
                self.start = self[1] 
        elif index == list_length - 1: 
            node_before = self[index-1]
            node_before.next = None
            self.end = node_before
        else: 
            node_before = self[index-1] 
            node_after = self[index+1] 
            node_before.next = node_after 
        return node_to_remove


class Variable(Object):                 # Переменная. Может хранить число
    def __init__(self, name, data: Object):   
        self.type = data.type
        self.name: str = name           
        self.data: Object = data

    def __repr__(self):
        return f'v#{self.name}=' + str(self.data)


class Storage():
    def __init__(self, variables: dict[str, Variable]={}):
        self.variables = variables

    def add(self, varaiable) -> None:
        self.variables[variable.name] = variable

    def remove(self, name) -> None:
        if self.declared:
            del self.variables[name]

    def get(self, name) -> Variable:
        var = self.variables.get(name, None)
        return var

    def declared(self, name) -> bool:
        if self.get(name):
            return True
        return False

    def type(self, name) -> str:
        if self.declared(name):
            return self.get(name).type
        return ''



class Operation():                                                  # Класс для осуществления и менеджмента

    def equate(lop: Object, rop: Object) -> Object: #!!!!!!!!!!!!!
        lop.data = rop.data
        return lop

    def addeq(lop: Object, rop: Object) -> Object: #!!!!!!!!!!!!!
        lop.data += rop.data
        return lop

    def subeq(lop: Object, rop: Object) -> Object: #!!!!!!!!!!!!!
        lop.data -= rop.data
        return lop

    def muleq(lop: Object, rop: Object) -> Object: #!!!!!!!!!!!!!
        lop.data *= rop.data
        return lop

    def diveq(lop: Object, rop: Object) -> Object: #!!!!!!!!!!!!!
        lop.data /= rop.data
        return lop


    operations: dict[str, ()] = {
            '=': equate, 
            '+=': addeq,
            '-=': subeq,
            '*=': muleq,
            '/=': diveq,

            '+': lambda lop, rop: Integer(lop.data + rop.data),
            '-': lambda lop, rop: Integer(lop.data - rop.data),
            '*': lambda lop, rop: Integer(lop.data * rop.data),
            '/': lambda lop, rop: Integer(lop.data / rop.data),

            '<': lambda lop, rop: Integer(lop.data < rop.data),
            '>': lambda lop, rop: Integer(lop.data > rop.data),
            '<=': lambda lop, rop: Integer(lop.data <= rop.data),
            '>=': lambda lop, rop: Integer(lop.data >= rop.data),
            '==': lambda lop, rop: Integer(lop.data == rop.data),
            }

    types: dict[str, object] = {
            'integer': Integer,
            'string': String,
            'float': Float,
            'list': List
            }
    
    @classmethod
    def get(cls, operation: str):
        return cls.operations[operation]









if __name__ == '__main__':
    l = Variable('lst', List())
    a1 = Variable('a1', Integer(11))
    a2 = Variable('a2', String('aboba'))
    l.data.append(a1)
    l.data.append(a2)
    #l.data.append(a2)
    print(l)





