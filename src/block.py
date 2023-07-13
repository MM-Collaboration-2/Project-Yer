from object import Object
from integer import Integer
from construction import Construction
from storage import Storage


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

