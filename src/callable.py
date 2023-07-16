from object import Object
from integer import Integer
from block import Block
from storage import Storage


class Function(Object):
    regex: str = ''
    type: str = 'function'
    specification: str = 'userdefined'

    def __init__(self, block: Block):
        self.block = block

    def run(self) -> Object:
        obj: Object = self.block.run()
        return obj
        
    def get_block(self) -> Block:
        return self.block

    def __repr__(self):
        return 'fn#'

class BuiltIn(Object):
    regex: str = ''
    type: str = 'function'
    specification: str = 'builtin'

    def __init__(self, function: callable):
        self.function: callable = function

    def run(self, arguments: list[Object], storage: Storage) -> Object:
        obj: Object = self.function(arguments, storage)
        return obj
        
    def __repr__(self):
        return 'builtin#'




if __name__ == '__main__':
    text = '''
Func(foo){
    Expr{b="b"}
    Expr{return b}
}
Expr{foo()}
'''
       
