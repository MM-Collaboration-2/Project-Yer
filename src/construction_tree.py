from re import search, compile
from constructions import *




class Node():
    def __init__(self, data: str, subnodes: list[Node]=[]):
        self.data: str = data
        self.subnodes: list[Node] = subnodes
        self.variables = {}

    def __repr__(self):
        return str(self.data) + ':' + str(self.subnodes)



class ConstructionTree():

    # Регулярка для нахождения первой конструкции что попадется
    pattern = compile('|'.join(_ for _ in CONSTRUCTIONS_TYPES.keys()))

    def __init__(self, text: str):
        self.text = text
        self.root = self.parse(self.text, 'Main')
        self.storage: Storage = Storage({})


    def parse(self, text: str, header: str):
        node = Node(header, [])                         # заголовок конструкции

        while len(text) > 0:

            m = search(self.pattern, text)
            new_header = text[m.start():m.end()]        # заголовок новой конструкции
            start_body = end_body = m.end()
            stack = Stack()

            while end_body < len(text) - 1:             # находим конец данной конструкции
                if text[end_body] == '{':
                    stack.push('{')
                elif text[end_body] == '}':
                    stack.pop()
                    if stack.is_empty():
                        break
                end_body += 1

            # если найденная конструкция -- выражение
            # добавляем ноду с выражением. В глубину не парсим
            if new_header == 'Expr':
                new_node = Node(text[m.start():end_body+1], [])

            # если любая другая конструкция
            # парсим ее в глубину
            else:
                new_node = self.parse(text[start_body+1:end_body], new_header)

            node.subnodes.append(new_node)

            # удаляем обработанную часть текста
            # идем дальше
            text = text[end_body+1:]

        return node

    def run(self):
        return self.reduce().run()


    def reduce(self):
        return self.__reduce(self.root, self.storage)

    @classmethod
    def __reduce(cls, node: Node, storage: Storage) -> Construction:
        if node.data.startswith('Expr'):
            obj = ExpressionBlock(node.data, storage)
            return obj
        else:
            lst = [cls.__reduce(n, storage) for n in node.subnodes]
            obj: Construction = Builder.create_construction(node.data, lst, storage)
            return obj


    
    def print(self):
        self.__print(self.root)

    @classmethod
    def __print(cls, node: Node, t=0):
        if node.data.startswith('Expr'):
            print('    '*t, f'{node.data}')
        else:
            print('    '*t, node.data, '{')
            for n in node.subnodes:
                cls.__print(n, t+1)
            print('    '*t, '}')


if __name__ == '__main__':
    text = '''
Expr{a=0}
While(a<12){
Expr{a=a+1}
}
Expr{a=a-0}
    '''
    text = text.replace('\n', '').replace(' ', '')
    t = ConstructionTree(text)
    t.print()
    #t.reduce()
    #print(t.run())
