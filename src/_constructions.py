from re import search
from construction import Construction
from stack import Stack
from utils import infix_to_postfix, token_type, syntax_analysis
from object import Object
from integer import Integer
from list import List
from operation import Operation
from storage import Storage



class Expression(Construction):                                     # Выражение состоит из одного или нескольких базовых выражений
    name: str = 'Exprssion'
    def __init__(self, stringg: str, storage: Storage):
        self.storage: Storage = storage
        self.stringg: str = stringg
        self.postfix: list[str] = infix_to_postfix(self.clear())

    def clear(self):
        if self.stringg.startswith('Expr{'):
            return self.stringg[:-1].replace('Expr{', '')
        return self.stringg
        
    def run(self):                                                  # создаем конвейер из элементарных выражений
        result: Object
        stack: Stack = Stack()
        for token in self.postfix:
            tok_type = token_type(token)

            if tok_type == 'operation':                             # если переменная если оператор -- создаем базовую операцию
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
                stack.push(result)                                  # помещаем результат выражения в обратно в стек
            else:


                obj = self.validate_operand(token, tok_type, self.storage)  # чтобы возвращать последний добавленный операндб в случае если
                                                                            # экспрешн состоит из одного операнда
                result = obj
                
                stack.push(obj)                                     # помещаем в стек

        return result                                               # для использования в условиях и циклах

    @classmethod
    def validate_list(cls, stringg: str, storage: Storage) -> List:
        lst = []

        # очистка от скобочек
        if stringg.startswith('['):
            stringg = stringg[1:]
        if stringg.endswith(']'):
            stringg = stringg[:-1]

        objects = tokens(stringg)
        for token in objects:
            tok_type = token_type(token)
            lst.append(cls.validate_operand(token, tok_type, storage))
        return List(lst)

    @classmethod
    def validate_variable(cls, token, storage: Storage):
        if storage.declared(token):
            variable: Variable = storage.get(token)

        else:
            variable: Variable = Variable(token, Integer(0)) # создаем новую
            storage.add(variable);
        
        return variable
    

    @classmethod
    def validate_operand(cls, token, tok_type, storage: Storage) -> Object:

        if tok_type == 'variable':
            var = cls.validate_variable(token, storage)
            return var

        elif tok_type == 'function':



            token: str = token[token.find('(')+1:-1]
            argument_list = cls.validate_list(token, storage).data
            storage.set_arguments(argument_list)


            ########
            if token.startswith('yell'):
                lst = token[:-1].replace('yell(', '')
                lst = cls.validate_list(lst, storage)
                for obj in lst.data:
                    print(obj)
                return Integer(len(lst.data))
            return Integer(0)
            #######

        elif tok_type == 'list':
            lst = cls.validate_list(token, storage)
            return lst

        elif tok_type == 'argument':
            num = int(token[-1])
            obj = storage.get_argument(num)
            return obj
        
        else:
            obj: Object = cls.basic_object(token, tok_type)
            return obj

    @classmethod
    def basic_object(cls, token: str, tok_type: str) -> Object:
        obj = BASIC_TYPES[tok_type](token)
        return obj


    def __repr__(self):
        return f'{self.stringg};'


class ExpressionBlock(Construction):
    regex: str = "Expr"
    name: str = 'Expr'
    def __init__(self, stringg: str, storage: Storage):
        self.storage: Storage = storage
        self.stringg: str = stringg
        self.expressions: list[Expression] = self.stringg_to_expressions()

    def stringg_to_expressions(self):
        stringg = self.clear()
        expressions: list[str] = [s for s in stringg.split(';') if s]
        expressions = [Expression(e, self.storage) for e in expressions] 
        return expressions

    def clear(self):
        if self.stringg.startswith('Expr{'):
            return self.stringg[:-1].replace('Expr{', '')
        return self.stringg

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
    regex:str = 'Block'
    def __init__(self, constructions: list[Construction], storage: Storage):
        self.storage: Storage = storage
        self.constructions: list[Construction] = constructions
        self.name: str = 'Block'

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
    regex: str = 'If\(.*?\)'
    name = 'If'
    def __init__(self, header: str, block: Block, storage: Storage):
        self.storage: Storage = storage
        self.header = header
        self.check_expression = self.get_check_expression()
        self.block = block

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
        return f'{self.header}\n{block}'


class While(Construction):
    regex: str = 'While\(.*?\)'
    name = 'While'
    def __init__(self, header: str, block: Block, storage: Storage):
        self.storage: Storage = storage
        self.header = header
        self.check_expression = self.get_check_expression()
        self.block = block

    def run(self) -> Object:
        result: Object = Integer(0)
        while True:
            flag = self.check_expression.run().data         # to get real int, not object
            if flag:
                result = self.block.run()
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
        block = str(self.block)
        return f'{self.header}\n{block}'


class For(Construction):
    regex: str = 'For\(.*?\)'
    name = 'For'
    def __init__(self, header: str, block: Block, storage: Storage):
        self.storage: Storage = storage
        self.header = header
        self.block = block
        self.init_expressions()

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
        block = str(self.block)
        return f'{self.header}\n{block}'

class Main(Block):
    regex :str = 'Main'
    name: str = 'Main'

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.constructions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block

class Function(Construction): # не обязана наследоваться от конструкции. можно в парсинге дерева добавлять в хранилище
    regex: str = 'Func\(.*?\)'
    name: str = 'Func'

    def __init__(self, text: str):
        self.validate(text)

    def validate(self, text: str):
        m = search(self.regex, text)

        self.head: str = text[m.start():m.end()-1].replace('Func(', '')
        self.text: str = syntax_analysis(text[m.end()+1:-1])

    def __repr__(self):
        return 'fn#' + self.head

global CONSTRUCTIONS_OBJECTS
CONSTRUCTIONS_OBJECTS = [ExpressionBlock, Block, If, While, For, Main, Function]
global CONSTRUCTIONS_HEADS
CONSTRUCTIONS_HEADS = {c.name: c for c in CONSTRUCTIONS_OBJECTS}
global CONSTRUCTIONS_TYPES
CONSTRUCTIONS_TYPES = {c.regex: c for c in CONSTRUCTIONS_OBJECTS}


if __name__ == '__main__':
    pass
