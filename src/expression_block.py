from construction import Construction
from storage import Storage
from expression import Expression
from integer import Integer
from void import Void


class ExpressionBlock(Construction):
    regex: str = "Expr"
    name: str = 'Expr'
    def __init__(self, string: str, storage: Storage, result_flag: bool=False):
        self.storage: Storage = storage
        self.string: str = string
        self.result_flag = result_flag
        self.expressions: list[Expression] = self.string_to_expressions()

    def string_to_expressions(self):
        string = self.clear()
        expressions: list[str] = [s for s in string.split(';') if s]
        expressions = [Expression(e, self.storage, self.result_flag) for e in expressions] 
        return expressions

    def clear(self):
        if self.string.startswith('Expr{'):
            return self.string[:-1].replace('Expr{', '')
        return self.string

    def run(self):
        result: Object = Void()
        for expression in self.expressions:
            result = expression.run()
            if result.type != 'void':
                break
        return result

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.expressions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block

