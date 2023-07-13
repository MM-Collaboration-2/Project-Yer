from block import Block


class Main(Block):
    regex :str = 'Main'
    name: str = 'Main'

    def __repr__(self):
        block = '\n'.join(str(c) for c in self.constructions)
        block =  f'{self.name}' +'{' + f'\n{block}\n' + '}'
        return block
