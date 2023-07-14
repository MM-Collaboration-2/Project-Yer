from object import Object
from void import Void
from integer import Integer
from construction import Construction


class Block(Construction):
    regex:str = 'Block'
    name: str = 'Block'
    def __init__(self, constructions: list[Construction]):
        self.constructions: list[Construction] = constructions

    def run(self):
        result: Object = Void()
        for construction in self.constructions:
            result = construction.run()
        return result

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.constructions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block

