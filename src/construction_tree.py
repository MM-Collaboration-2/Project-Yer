from re import search, compile
from utils import syntax_analysis
from stack import Stack
from storage import Storage 
from construction import Construction
from expression_block import ExpressionBlock
from construction_types import CONSTRUCTIONS_TYPES
from builder import Builder


class Node():
    def __init__(self, data: str, subnodes=[]):
        self.data: str = data
        self.subnodes = subnodes
        self.variables = {}

    def __repr__(self):
        return str(self.data) + ':' + str(self.subnodes)



class ConstructionTree():

    # Регулярка для нахождения первой конструкции что попадется
    pattern = compile('|'.join(_ for _ in CONSTRUCTIONS_TYPES.keys()))

    def __init__(self, text: str, storage: Storage):
        self.text = text
        self.root = self.parse(self.text, 'Main')
        self.storage: Storage = storage


    def end_body(self, text) -> int:
        index = 0
        bracket_stack = Stack()
        quotes_stack = Stack()

        while index < len(text) - 1:                # находим конец данной конструкции

            if text[index] == '\"':                 # если кавычка
                if quotes_stack.is_empty():         # и стек пустой
                    quotes_stack.push(text[index])  # тудааааа её
                else:
                    quotes_stack.pop()              # иначе есвобождаем стек

            if quotes_stack.is_empty():             # только если стек кавычек пуст
                if text[index] == '{':              # обрабатываем на наличие скобок
                    bracket_stack.push('{')

                elif text[index] == '}':
                    bracket_stack.pop()

                    if bracket_stack.is_empty():
                        break
            index += 1
        
        return index


    def parse(self, text: str, header: str):
        node = Node(header, [])                         # заголовок конструкции
        ###
        #print(text)

        while len(text) > 0:

            m = search(self.pattern, text)
            new_header = text[m.start():m.end()]        # заголовок новой конструкции
            start_body = end_body = m.end()
            stack = Stack()

            end_body = self.end_body(text)             # находим конец данной конструкции

            # если найденная конструкция -- выражение
            # добавляем ноду с выражением. В глубину не парсим
            if new_header.startswith('Expr') or new_header.startswith('Func'):
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
    Expr{b=2}
    While(a<5){
        Expr{a=a+1;
            b=b+2;
            yell(["aboba"]);
        }
    }
        '''
    text = syntax_analysis(text)
    s = Storage({})
    t = ConstructionTree(text, s)
    #t.print()
    # print(t.reduce())
    print(t.run())
