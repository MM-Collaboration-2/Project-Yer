## Yer basic objects

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


class Node(Object):
    regex = ''
    type: str = 'list_node'
    def __init__(self, data: Object):
        self.data = data
        self.next = None

    def __repr__(self):
        return f'n#' + str(self.data)


class List(Object):
    regex = '\[.*\]'
    type: str = 'list'
    def __init__(self, elements=None):
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


class Variable(Object):                     # Хранит объект
    regex = '[\u263a-\U0001f645а-яА-Яa-zA-Z][\u263a-\U0001f645а-яА-Яa-zA-Z0-9_]*'
    type: str = 'variable'
    def __init__(self, name, obj: Object = Object()):   
        self.name: str = name           
        self.obj: Object = obj

    def __repr__(self):
        return f'v#{self.name}=' + str(self.obj)


global BASIC_OBJECTS
BASIC_OBJECTS: list[Object] = [Integer, Float, String, List]
global BASIC_TYPES
BASIC_TYPES: dict[str: Object] = {obj.type: obj for obj in BASIC_OBJECTS}



if __name__ == '__main__':
    s1 = String('"a"')
    s2 = String('"b"')

    print(s1.data + s2.data)
