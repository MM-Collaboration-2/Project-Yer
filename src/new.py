from re import fullmatch, match, search, findall



class Node(data: Construction):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def set_left(node):
        self.left = node

    def set_right(node):
        self.right = node


class ConstructionTree():
    def __init__(self, root=None):
        self.root = root

    def parse(text):







class Object():
    def __init__(self, data=0):
        self.type: str = 'object'
        self.data: int = 0

    def __str__(self):
        return str(self.data)

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
    def equate(lop: Object, rop: Object) -> Int: #!!!!!!!!!!!!!
        lop.data = rop.data
        return lop

    def addeq(lop: Object, rop: Object) -> Int: #!!!!!!!!!!!!!
        lop.data += rop.data
        return lop

    def subeq(lop: Object, rop: Object) -> Int: #!!!!!!!!!!!!!
        lop.data -= rop.data
        return lop

    def muleq(lop: Object, rop: Object) -> Int: #!!!!!!!!!!!!!
        lop.data *= rop.data
        return lop

    def diveq(lop: Object, rop: Object) -> Int: #!!!!!!!!!!!!!
        lop.data /= rop.data
        return lop


    operations: dict[str, ()] = {
            '=': equate, 
            '+': lambda lop, rop: Int(lop.data + rop.data),
            '-': lambda lop, rop: Int(lop.data - rop.data),
            '*': lambda lop, rop: Int(lop.data * rop.data),
            '/': lambda lop, rop: Int(lop.data / rop.data),
            
            '+=': addeq,
            '-=': subeq,
            '*=': muleq,
            '/=': diveq,

            '==': lambda lop, rop: Int(lop.data == rop.data),
            '<': lambda lop, rop: Int(lop.data < rop.data),
            '<=': lambda lop, rop: Int(lop.data <= rop.data),
            '>': lambda lop, rop: Int(lop.data > rop.data),
            '>=': lambda lop, rop: Int(lop.data >= rop.data),
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
        self.name = 'basic_expression'

    def run(self):
        return Operation.get(self.op)(self.lop, self.rop)

    def __str__(self):
        lop = str(self.lop)
        rop = str(self.rop)
        op = self.op
        return f'{lop} {op} {rop}'


class Expression(Construction):
    def __init__(self, expression, variables):
        self.expression = expression
        self.postfix = infix_to_prefix(expression)
        self.variables = variables
        self.name = 'expression'
        
    def run(self):                                                  # создаем конвейер из элементарных выражений
        result: Int
        object_stack: Stack = Stack()
        for token in self.postfix:
            if fullmatch('[+-]?\d+', token):                        # если число -- добавляем число
                object_stack.push(Int.from_string(token))           # помещаем в стек
            elif fullmatch('[a-zA-Z][a-zA-Z0-9_]*', token):         # если переменная
                if token not in self.variables.keys(): 
                    self.variables[token] = Variable(token)         # создаем переменную если не существует
                object_stack.push(self.variables[token])            # помещаем в стек
            elif fullmatch('[<>+\-*/=]=?', token):                      # если оператор -- создаем базовую операцию
                rop = object_stack.pop()
                lop = object_stack.pop()
                op = token
                basic_expression = BasicExpression(lop, rop, op)    # создаем базовую операцию
                result = basic_expression.run()
                object_stack.push(result)                           # помещаем результат выражения в обратно в стек

        return result

class Block(Construction):
    def __init__(self, constructions: list[Construction], variables):
        self.constructions = constructions
        self.variables: dict = variables
        self.name: str = 'block'

    def run(self):
        for construction in self.constructions:
            construction.run()


class If(Construction):
    def __init__(self, check_expression: Expression, block: Block):
        self.check_expression = check_expression
        self.block = block

    def run(self):
        if self.check_expression.run():
            self.block.run()


class While(Construction):
    def __init__(self, check_expression: Expression, block: Block):
        self.check_expression = check_expression
        self.block = block

    def run(self):
        while True:
            flag = self.check_expression.run()
            if flag:
                self.block.run()
            else:
                break
        

def _parse(text: str):
    constructions = {'Expr{': Expression,           # Все возможные конструкции
                     'If{': If,
                     'For{': For,
                     'While{': While,
                     }

    pattern = '|'.join(_ for _ in constructions.keys())   # Регулярка для нахождения первой конструкции что попадется

    m = re.match(pattern, text)
    start, end = m.start(), m.end()
    obj = constructions[text[start:end]]
    
    index = end + 1
    while text[index] != '}':
        if text[index] == '(':
            return parse(text[end+1:index])
        index += 1

    obj = obj(text[start:index])
    print(obj)
    return obj(text[start:index])

def parse(text: str):
    #text = text.strip()
    constructions = ['Block{',           # Все возможные конструкции
                     'If{',
                     'For{',
                     'While{',
                     #'Expr{',
                     ]

    pattern = '|'.join(_ for _ in constructions)   # Регулярка для нахождения первой конструкции что попадется

    m = search(pattern, text)
    if m is None:
        return
    start, end = m.start(), m.end()
    obj = text[start:end]
    index = end
    stack = Stack()
    while index < len(text) - 1:
        index += 1
        if text[index] == '{':
            stack.push('{')
        elif text[index] == '}':
            if not stack.is_empty():
                stack.pop()
            if stack.is_empty():
                parse(text[end:index+1])
                break

    print(text)
    


text = '''
Block{ 
    If{
        For{
            Expr{}
        }
        Expr{}
    }
    Expr{}
}
'''
text = text.replace('\n', '').replace(' ', '')
parse(text)


def main():
    global variables
    variables = {}
    while True:
        inp = input('>>> ')
        if len(inp) == 0:
            continue
        elif len(inp) == 1:
            outp = variables.get(inp, inp)
        else:
            exp = Expression(inp, variables)
            outp = exp.run()
        print(outp)

if __name__ == '__main__':
    pass
    #main()

#variables = {}
#
#e1 = Expression("a = 2", variables)
#e1.run()
#e2 = Expression("a = a + 2", variables)
#e3 = Expression("a < 3", variables)
#block = Block([e1, e2], variables)
#_if = If(e3, block)
#_if.run()
#print(variables['a'])

