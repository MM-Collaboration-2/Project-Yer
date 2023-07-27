from object import Object
from void import Void
from integer import Integer
from storage import Storage
from construction import Construction
from expression import Expression
from block import Block
from utils import get_header_expressions, smart_split_semi


class If(Construction):
    regex: str = 'If\ *\(.*?\)\ *{'
    name = 'If'
    def __init__(self, header: str, block: Block, storage: Storage):
        self.storage: Storage = storage
        self.header = header
        self.check_expression = self.get_check_expression()
        self.block = block

    def get_check_expression(self) -> Expression:
        return Expression(get_header_expressions(self.header), self.storage, True)

    def run(self) -> Object:
        result: Objcet = Void()
        if self.check_expression.run().data:
            result = self.block.run()
        return result

    def __repr__(self):
        exp = str(self.check_expression)
        block = str(self.block)
        return f'{self.header}\n{block}'


class While(Construction):
    regex: str = 'While\ *\(.*?\)\ *{'
    name = 'While'
    def __init__(self, header: str, block: Block, storage: Storage):
        self.storage: Storage = storage
        self.header = header
        self.check_expression = self.get_check_expression()
        self.block = block

    def run(self) -> Object:
        result: Object = Void()
        while True:
            flag = self.check_expression.run().data         # to get real int, not object
            if flag:
                result = self.block.run()
            else:
                break
        return result
        
    def get_check_expression(self) -> Expression:
        return Expression(get_header_expressions(self.header), self.storage, True)

    def __repr__(self):
        block = str(self.block)
        return f'{self.header}\n{block}'


class For(Construction):
    regex: str = 'For\ *\(.*?\)\ *{'
    name = 'For'
    def __init__(self, header: str, block: Block, storage: Storage):
        self.storage: Storage = storage
        self.header = header
        self.block = block
        self.init_expressions()

    def run(self) -> Object:
        self.init_expression.run()
        result: Object = Void()
        while True:
            flag = self.check_expression.run().data         # to get real int, not object
            if flag:
                result = self.block.run()
                self.increment_expression.run()
            else:
                break
        return result
                
    def init_expressions(self):
        expressions = smart_split_semi(get_header_expressions(self.header))
        expressions = [Expression(e, self.storage, True) for e in expressions]
        self.init_expression = expressions[0]
        self.check_expression = expressions[1]
        self.increment_expression = expressions[2]

    def clear(self):
        if self.header.startswith('For('):
            return self.header[:-2].replace('For(', '')
        return self.header

    def __repr__(self):
        block = str(self.block)
        return f'{self.header}\n{block}'

