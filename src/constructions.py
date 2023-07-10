from re import fullmatch, compile, match
from utils import infix_to_postfix, token_type
from basic import *




class Construction():
    def __repr__(self):
        return 'construction'


class BasicExpression(Construction):                                # Базооваое выражение. Все выражения сводятся к ним.
    def __init__(self, lop, rop, op):
        self.lop: Integer = lop
        self.rop: Integer = rop
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
        self.variables: dict = variables
        self.string: str = string
        self.postfix: list[str] = infix_to_postfix(self.clear())
        self.name: str = 'expression'

    def clear(self):
        if self.string.startswith('Expr{'):
            return self.string[:-1].replace('Expr{', '')
        return self.string
        
    def run(self):                                                  # создаем конвейер из элементарных выражений
        result: Integer
        object_stack: Stack = Stack()
        for token in self.postfix:
            tok_type = token_type(token)

            if tok_type == 'number':                              # если число -- добавляем число
                object_stack.push(Integer(token))           # помещаем в стек

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

    def __repr__(self):
        return f'{self.name} {self.string};'


class ExpressionBlock(Construction):
    def __init__(self, string: str, variables: dict):
        self.variables: dict = variables
        self.string: str = string
        self.expressions: list[Expression] = self.string_to_expressions()
        self.name: str = 'expression block'

    def string_to_expressions(self):
        string = self.clear()
        expressions: list[str] = [s for s in string.split(';') if s]
        expressions = [Expression(e, self.variables) for e in expressions] 
        return expressions

    def clear(self):
        if self.string.startswith('Expr{'):
            return self.string[:-1].replace('Expr{', '')
        return self.string

    def run(self):
        result: Integer
        for expression in self.expressions:
            result = expression.run()
        return result

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.expressions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block


class Block(Construction):
    def __init__(self, constructions: list[Construction], variables: dict):
        self.variables: dict = variables
        self.constructions: list[Constructio] = constructions
        self.name: str = 'block'

    def run(self):
        result: Integer
        for construction in self.constructions:
            result = construction.run()
        return result

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.constructions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block


class If(Construction):
    def __init__(self, header: str, block: Block, variables: dict):
        self.variables = variables
        self.header = header
        self.check_expression = self.get_check_expression()
        self.block = block
        self.name = 'if'

    def get_check_expression(self) -> Expression:
        return Expression(self.clear(), self.variables)

    def clear(self):
        if self.header.startswith('If('):
            return self.header[:-1].replace('If(', '')
        return self.header

    def run(self):
        if self.check_expression.run().data:
            return self.block.run()

    def __repr__(self):
        exp = str(self.check_expression)
        block = str(self.block)
        return f'{self.name}\n{exp}\n{block}'


class While(Construction):
    def __init__(self, header: str, block: Block, variables: dict):
        self.variables = variables
        self.header = header
        self.check_expression = self.get_check_expression()
        self.block = block
        self.name = 'while'

    def run(self):
        while True:
            flag = self.check_expression.run().data         # to get real int, not object
            if flag:
                self.block.run()
            else:
                break
        
    def get_check_expression(self) -> Expression:
        return Expression(self.clear(), self.variables)

    def clear(self):
        if self.header.startswith('While('):
            return self.header[:-1].replace('While(', '')
        return self.header

    def __repr__(self):
        exp = str(self.check_expression)
        block = str(self.block)
        return f'{self.name}{exp}\n{block}'


# FIXME работает неправильно
class For(Construction):
    def __init__(self, header: str, block: Block, variables: dict):
        self.variables = variables
        self.header = header
        self.block = block
        self.init_expressions()
        self.name = 'for'

    def run(self):
        self.init_expression.run()
        while True:
            flag = self.check_expression.run().data         # to get real int, not object
            if flag:
                self.block.run()
                self.increment_expression.run()
            else:
                break
                
    def init_expressions(self):
        expressions = [s for s in self.clear().split(';') if s]
        expressions = [Expression(e, self.variables) for e in expressions]
        self.init_expression = expressions[0]
        self.check_expression = expressions[1]
        self.increment_expression = expressions[2]

    def clear(self):
        if self.header.startswith('For('):
            return self.header[:-1].replace('For(', '')
        return self.header

    def __repr__(self):
        exp = str(self.check_expression)
        block = str(self.block)
        return f'{self.name}{exp}\n{block}'


class Main(Block):
    pass


if __name__ == '__main__':
    v = {}
    exp1 = ExpressionBlock('Expr{a=1;}', v);
    header = 'While(a < 8)'
    exp2 = ExpressionBlock('Expr{a=a+1}', v);
    b1 = Block([exp1], v)
    b2 = Block([exp2], v)

    b1.run()
    w = While(header, b2, v)
    w.run()
    print(v['a'])
    #print(v['b'])



