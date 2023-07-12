from re import search
from basic_structures import Object
from storage import Storage
from constructions import Block

class Function(): # не обязана наследоваться от конструкции. можно в парсинге дерева добавлять в хранилище
    regex: str = 'Func\(.*?\)'
    name: str = 'Func'

    def __init__(self, text: str):
        self.validate(text)

    def validate(self, text: str):
        m = search(self.regex, text)

        self.head: str = text[m.start():m.end()-1].replace('Func(', '')
        self.text: str = text[m.end():]


    def run(self, params: list[str], storage: Storage):
        block = self.get_block(params, storage)
        return block.run()
        

    def get_block(self, params: list[str], storage: Storage) -> Block:
        block: Block = ConstructionTree(self.substitute(params), storage).reduce()
        return block


    def substitute(self, params: list[str]) -> str:
        text = self.text
        for num, param in enumerate(params):
            arg_name = 'argv#' + str(num)
            text = text.replace(arg_name, param)

        
        return text

    def __repr__(self):
        return 'fn#' + self.head



if __name__ == '__main__':
    text = '''
Func(foo){
    While(argv#0>3){
        Expr{argv#0=argv#0-2;
            b=b+argv#1;
            b
        }
    }
}
'''

    f = Function(text)
    l = ['c', 'd', 'e']
    s = Storage({})
    f.run(l, s)
