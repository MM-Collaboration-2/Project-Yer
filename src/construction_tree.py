from re import search, compile
from utils import syntax_analysis
from stack import Stack
from storage import Storage 
from construction import Construction
from expression_block import ExpressionBlock
from construction_types import CONSTRUCTIONS_TYPES
from builder import Builder
from yer_builtins import BUILTINS


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

            ###### выражения после найденной конструкции
            if m is None:
                node.subnodes.append(Node(text, []))
                return node
            ######

            new_header = text[m.start():m.end()]        # заголовок новой конструкции
            start_body = end_body = m.end()
            stack = Stack()

            end_body = self.end_body(text)             # находим конец данной конструкции


            ####### выражения до найденной конструкции
            if len(text[:m.start()]) > 0:
                node.subnodes.append(Node(text[:m.start()], []))
            #######

            # если найденная конструкция -- выражение
            # добавляем ноду с выражением. В глубину не парсим
            if new_header.startswith('Expr'):
                new_node = Node(text[m.start():end_body+1], [])

            # если функция
            elif new_header.startswith('Func'):
                new_node = self.parse(text[start_body+1:end_body], new_header)

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
    Func(add){
        Expr{return $argv0+$argv1;}
    }
    Expr{
        l = [1, 2, 3];
        b = 1;
        v = get(l, b);
        yell(v)
    }
    '''
    
    text1 = '''
    Func(fib){
        a = 0;
        b = 1;
        c = 0;
        For(i=0;i<$argv0;i=i+1){
            c = a + b;
            a = b;
            b = c;
        }
        c = 43;c=c+12;
        return c;
    }
    r = fib(6);
    yell(r);
    '''
    text = syntax_analysis(text1)
    s = Storage(BUILTINS, Stack())
    t = ConstructionTree(text, s)
    b = t.reduce()

    t.run()
    
