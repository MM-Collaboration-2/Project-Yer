from re import fullmatch, compile, match
from utils import infix_to_postfix, token_type
from basic_structures import *
from service_structures import *



class Construction():
    def __repr__(self):
        return 'construction'


class Expression(Construction):                                     # Выражение состоит из одного или нескольких базовых выражений
    def __init__(self, string: str, storage: Storage):
        self.storage: Storage = storage
        self.string: str = string
        self.postfix: list[str] = infix_to_postfix(self.clear())
        self.name: str = 'expression'

    def clear(self):
        if self.string.startswith('Expr{'):
            return self.string[:-1].replace('Expr{', '')
        return self.string
        
    def run(self):                                              # создаем конвейер из элементарных выражений
        result: Integer
        stack: Stack = Stack()
        for token in self.postfix:
            tok_type = token_type(token)

            if tok_type == 'operation':                       # если переменная если оператор -- создаем базовую операцию
                rop = stack.pop()
                lop = stack.pop()
                op = token
                
                result = Operation.run(lop, rop, op, self.storage)
                # Здесь валидировать операнды
                # так как результат операции возвращается обратно в стек
                # т.е. тип возвращаемого операцией объекта
                # должен быть таким же как и тип объектов в стеке
                # -- строка или Object.
                # Конвертить строку в объект потом обратно в строку 
                # чтобы засунутть в стек неоч логично
                # лучше уж на ходу здесь токены в объекты валидировать
                #result = basic_expression.run()
                stack.push(result)                              # помещаем результат выражения в обратно в стек
            else:
                # Фнукция создания объекта из строки
                # одна, универсальная
                obj = self.validate_operand(token, tok_type, self.storage)
                stack.push(obj)                               # помещаем в стек

        return result # для использования в условиях и циклах


    @classmethod
    def validate_operand(cls, token, tok_type, storage: Storage) -> Object:

        if tok_type == 'variable':

            if storage.declared(token):
                variable: Variable = storage.get(token)

            else:
                variable: Variable = Variable(token, Integer(0))
                storage.add(variable);
            
            return variable
        
        else:
            obj: Object = cls.basic_object(token, tok_type)
            return obj

    # Может это перенести в basic_structures?
    @classmethod
    def basic_object(cls, token: str, tok_type: str) -> Object:
        obj = BASIC_TYPES[tok_type](token)
        return obj

    def __repr__(self):
        return f'{self.name} {self.string};'


class ExpressionBlock(Construction):
    def __init__(self, string: str, storage: Storage):
        self.storage: Storage = storage
        self.string: str = string
        self.expressions: list[Expression] = self.string_to_expressions()
        self.name: str = 'expression block'

    def string_to_expressions(self):
        string = self.clear()
        expressions: list[str] = [s for s in string.split(';') if s]
        expressions = [Expression(e, self.storage) for e in expressions] 
        return expressions

    def clear(self):
        if self.string.startswith('Expr{'):
            return self.string[:-1].replace('Expr{', '')
        return self.string

    def run(self):
        result: Object = Integer(0)
        for expression in self.expressions:
            result = expression.run()
        return result

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.expressions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block


class Block(Construction):
    def __init__(self, constructions: list[Construction], storage: Storage):
        self.storage: Storage = storage
        self.constructions: list[Constructio] = constructions
        self.name: str = 'block'

    def run(self):
        result: Object = Integer(0)
        for construction in self.constructions:
            result = construction.run()
        return result

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.constructions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block


class If(Construction):
    def __init__(self, header: str, block: Block, storage: Storage):
        self.storage: Storage = storage
        self.header = header
        self.check_expression = self.get_check_expression()
        self.block = block
        self.name = 'if'

    def get_check_expression(self) -> Expression:
        return Expression(self.clear(), self.storage)

    def clear(self):
        if self.header.startswith('If('):
            return self.header[:-1].replace('If(', '')
        return self.header

    def run(self) -> Object:
        result = Integer(0)
        if self.check_expression.run().data:
            result = self.block.run()
        return result

    def __repr__(self):
        exp = str(self.check_expression)
        block = str(self.block)
        return f'{self.name}\n{exp}\n{block}'


class While(Construction):
    def __init__(self, header: str, block: Block, storage: Storage):
        self.storage: Storage = storage
        self.header = header
        self.check_expression = self.get_check_expression()
        self.block = block
        self.name = 'while'

    def run(self) -> Object:
        result: Object = Integer(0)
        while True:
            flag = self.check_expression.run().data         # to get real int, not object
            if flag:
                self.block.run()
            else:
                break
        return result
        
    def get_check_expression(self) -> Expression:
        return Expression(self.clear(), self.storage)

    def clear(self):
        if self.header.startswith('While('):
            return self.header[:-1].replace('While(', '')
        return self.header

    def __repr__(self):
        exp = str(self.check_expression)
        block = str(self.block)
        return f'{self.name}{exp}\n{block}'


class For(Construction):
    def __init__(self, header: str, block: Block, storage: Storage):
        self.storage: Storage = storage
        self.header = header
        self.block = block
        self.init_expressions()
        self.name = 'for'

    def run(self) -> Object:
        self.init_expression.run()
        result: Object = Integer(0)
        while True:
            flag = self.check_expression.run().data         # to get real int, not object
            if flag:
                result = self.block.run()
                self.increment_expression.run()
            else:
                break
        return result
                
    def init_expressions(self):
        expressions = [s for s in self.clear().split(';') if s]
        expressions = [Expression(e, self.storage) for e in expressions]
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
    s = Storage({})
    header = 'For(a=18;a>4;a=a-1)'
    exp1 = ExpressionBlock('Expr{}', s);
    exp2 = ExpressionBlock('Expr{}', s);
    b1 = Block([exp1], s)
    b2 = Block([exp2], s)

    b1.run()
    f = For(header, b2, s)
    f.run()
    print(s.get('a'))



