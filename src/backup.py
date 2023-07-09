from re import fullmatch





class Object():
    def __init__(self, data=0):
        self.type: str = 'object'
        self.data: int = 0

    def __str__(self):
        return str(self.data)

    #def __add__(self, other):
        #return self.data + other.data
#
    #def __sub__(self, other):
        #return self.data - other.data
#
    #def __mul__(self, other):
        #return self.data * other.data
#
    #def __div__(self, other):
        #return self.data / other.data
#
    #def __eq__(self, other):
        #return self.data == other.data


class Variable(Object):
    def __init__(self, name, data=0):
        self.type = 'variable'
        self.name: str = name
        self.data: int = data

    def __repr__(self):
        return f'Var {self.name} is {self.data}'

    def __str__(self):
        return str(self.data)

    #def __div__(self, other):
        #return self.data / other.data

class Int(Object):
    def __init__(self, number):
        self.type = "int"
        self.data = int(number)

    @classmethod
    def from_string(cls, string: str):
        number: int = int(string)
        return Int(number)

    #def __div__(self, other):
        #return self.data / other.data



class Stack():
    def __init__(self):
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


def infix_to_prefix(infixexpr):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    prec["="] = 1

    op_stack = Stack()
    postfix_list = []

    token_list = infixexpr.split()

    for token in token_list:
        if fullmatch('[+-]?\d+', token):           # если число
            postfix_list.append(token)
        elif fullmatch('[a-zA-Z][a-zA-Z0-9_]*', token): # есди переменная
            postfix_list.append(token)
        elif token == '(':
            op_stack.push( token)
        elif token == ')':
            top_token = op_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = op_stack.pop()

        else:
            while (not op_stack.is_empty()) and \
                (prec.get(op_stack.peek(), 1) >= prec.get(token, 1)):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.is_empty():
        postfix_list.append(op_stack.pop())
    return postfix_list

class Operation():
    def equate(lop: Object, rop: Object) -> Object:
        lop.data = rop.data
        return lop

    operations: dict[str, ()] = {
            '=': equate, 
            '+': lambda lop, rop: Int(lop.data + rop.data),
            '-': lambda lop, rop: Int(lop.data - rop),
            '*': lambda lop, rop: Int(lop.data * rop.data),
            '/': lambda lop, rop: Int(lop.data / rop.data),
            '==': lambda lop, rop: Int(lop.data == rop.data),
            }
    
    @classmethod
    def get(cls, operation: str):
        return cls.operations[operation]


class Construction():
    pass

class Pipeline():
    def __init__(self):
        self.pipeline = []

    def add(self, construction: Construction):
        self.pipeline.append(construction)

    def run(self):
        while self.pipeline:
            self.pipeline.pop(0).run()


class BasicExpression(Construction):
    def __init__(self, lop, rop, op):
        self.lop: Int = lop
        self.rop: Int = rop
        self.op: str = op

    def run(self):
        return Operation.get(self.op)(self.lop, self.rop)

    def __str__(self):
        lop = str(self.lop)
        rop = str(self.rop)
        op = self.op
        return f'{lop} {op} {rop}'


class Expression(Construction):
    def __init__(self, expression):
        self.expression = expression
        
    def run(self):                                                  # создаем конвейер из элементарных выражений
        result: Int
        object_stack: Stack = Stack()
        for token in self.expression:
            if fullmatch('[+-]?\d+', token):                        # если число -- добавляем число
                object_stack.push(Int.from_string(token))           # помещаем в стек
            elif fullmatch('[a-zA-Z][a-zA-Z0-9_]*', token):         # если переменная
                if token not in variables.keys(): 
                    variables[token] = Variable(token)              # создаем переменную если не существует
                object_stack.push(variables[token])                 # помещаем в стек
            elif fullmatch('[+\-*/=]', token):                      # если оператор -- создаем базовую операцию
                rop = object_stack.pop()
                lop = object_stack.pop()
                op = token
                basic_expression = BasicExpression(lop, rop, op)    # создаем базовую операцию
                result = basic_expression.run()
                object_stack.push(result)                           # помещаем результат выражения в обратно в стек

        return result



class If(Construction):
    pass



def main():
    global variables
    variables = {}
    while True:
        inp = input('>>> ')
        inp = infix_to_prefix(inp)
        if len(inp) == 0:
            continue
        elif len(inp) == 1:
            outp = variables.get(inp[0], inp[0])
        else:
            exp = Expression(inp)
            outp = exp.run()
        print(outp)

main()


'''
x = 1 + 2
'''
