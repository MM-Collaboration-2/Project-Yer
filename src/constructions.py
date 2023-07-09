from re import fullmatch
from utils import infix_to_postfix, token_type
from basic import *


class Operation():                                                  # Класс для осуществления и менеджмента
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
            '+=': addeq,
            '-=': subeq,
            '*=': muleq,
            '/=': diveq,

            '+': lambda lop, rop: Int(lop.data + rop.data),
            '-': lambda lop, rop: Int(lop.data - rop.data),
            '*': lambda lop, rop: Int(lop.data * rop.data),
            '/': lambda lop, rop: Int(lop.data / rop.data),

            '<': lambda lop, rop: Int(lop.data < rop.data),
            '>': lambda lop, rop: Int(lop.data > rop.data),
            '<=': lambda lop, rop: Int(lop.data <= rop.data),
            '>=': lambda lop, rop: Int(lop.data >= rop.data),
            '==': lambda lop, rop: Int(lop.data == rop.data),
            }
    
    @classmethod
    def get(cls, operation: str):
        return cls.operations[operation]


class Construction():
    def __repr__(self):
        return 'construction'


class Pipeline():
    def __init__(self):
        self.pipeline = []

    def add(self, construction: Construction):
        self.pipeline.append(construction)

    def run(self):
        while self.pipeline:
            self.pipeline.pop(0).run()


class BasicExpression(Construction):                                # Базооваое выражение. Все выражения сводятся к ним.
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


class Expression(Construction):                                     # Выражение состоит из одного или нескольких базовых выражений
    def __init__(self, string: str, variables: dict):
        self.string: str = string
        self.postfix: list[str] = infix_to_postfix(string)
        self.variables: dict = variables
        self.name: str = 'expression'

    def __repr__(self):
        return f'{self.name} {self.string};'

        
    def run(self):                                                  # создаем конвейер из элементарных выражений
        result: Int
        object_stack: Stack = Stack()
        for token in self.postfix:
            tok_type = token_type(token)

            if tok_type == 'number':                              # если число -- добавляем число
                object_stack.push(Int.from_string(token))           # помещаем в стек

            elif tok_type == 'variable':                          # если переменная

                if token not in self.variables.keys(): 
                    self.variables[token] = Variable(token)         # создаем переменную если не существует

                object_stack.push(self.variables[token])            # помещаем в стек

            elif tok_type == 'operation':                         # если переменная если оператор -- создаем базовую операцию
                rop = object_stack.pop()
                lop = object_stack.pop()
                op = token
                basic_expression = BasicExpression(lop, rop, op)    # создаем базовую операцию
                result = basic_expression.run()
                object_stack.push(result)                           # помещаем результат выражения в обратно в стек

        return result


class ExpressionBlock(Construction):
    def __init__(self, string: str, variables: dict):
        self.string: str = string
        self.variables: dict = variables
        self.expressions: list[Expression] = self.from_string()
        self.name: str = 'expression block'

    def from_string(self):
        string = self.string[:-1].replace('Expr{', '')                  # deleting 'Expr{}'
        expressions: list[str] = [s for s in string.split(';') if s]
        expressions = [Expression(e, self.variables) for e in expressions] 
        return expressions

    def run(self):
        for expression in self.expressions:
            expression.run()

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.expressions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block

class Block(Construction):
    def __init__(self, string: str, variables: dict):
        self.string: str = string
        self.variables: dict = variables
        self.expressions: list[Expression] = self.from_string()
        self.name: str = 'block'

    def from_string(self):
        string = self.string[:-1].replace('Block{', '')                  # deleting 'Block{}'
        expressions: list[str] = [s for s in string.split(';') if s]
        expressions = [Expression(e, self.variables) for e in expressions] 
        return expressions

    def run(self):
        result: Int
        for expression in self.expressions:
            result = expression.run()
        return result

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.expressions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block


class If(Construction):
    def __init__(self, check_expression: Expression, block: Block):
        self.check_expression = check_expression
        self.block = block
        self.name = 'if'

    def run(self):
        if self.check_expression.run():
            self.block.run()

    def __repr__(self):
        exp = str(self.check_expression)
        block = str(self.block)
        return f'{self.name}\n{exp}\n{block}'


class While(Construction):
    def __init__(self, check_expression: Expression, block: Block):
        self.check_expression = check_expression
        self.block = block
        self.name = 'while'

    def run(self):
        while True:
            flag = self.check_expression.run().data         # to get real int, not object
            if flag:
                self.block.run()
            else:
                break
        
    def __repr__(self):
        exp = '(' + str(self.check_expression) + ')'
        block = str(self.block)
        return f'{self.name}{exp}\n{block}'


class For(Construction):
    pass

class Main(Construction):
    pass


if __name__ == '__main__':
    v = {}
    s = 'Block{a = a + 1;}'
    b = Block(s, v)
    check_e = Expression('a < 1700', v)
    w = While(check_e, b)
    w.run()
    print(w)






