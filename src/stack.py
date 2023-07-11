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
