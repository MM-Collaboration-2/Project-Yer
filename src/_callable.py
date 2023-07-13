from object import Object
# from storage import Storage
# ему запрещено передавть стораж, чтобы он мог храниться в стораже
from block import Block
from function import Function
#from construction_tree import ConstructionTree


class Callable(Object):
    regex: str = ''
    type: str = 'function'

    def __init__(self, head: str, text: str):
        self.name = head
        self.text = text

    def run(self, params: list[str], storage: Storage):
        block = self.get_block(params, storage)
        return block.run()
        
    def get_block(self, params: list[str], storage: Storage) -> Block:
        t = ConstructionTree(self.substitute(params), storage)
        block = t.reduce()
        return block

    def substitute(self, params: list[str]) -> str:
        text = self.text
        for num, param in enumerate(params):
            arg_name = 'argv#' + str(num)
            text = text.replace(arg_name, param)
        return text

    def __repr__(self):
        return 'cl#' + self.name




if __name__ == '__main__':
    text = '''
Func(foo){
    Expr{b="b"}
    While(argv#0<3){
        Expr{argv#0=argv#0+2;
            b=b+"y";
            b
        }
    }
}
'''

    f = Function(text)
    l = ['c', 'd', 'e']
    s = Storage({})
    #print(f.get_block(l, s))
    print(f.run(l, s))
