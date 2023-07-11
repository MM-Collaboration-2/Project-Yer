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

    def __init__(self, root=None):
        self.root = Node('Main')


    def parse(text: str, header: str):
        node = Node(header, [])                         # заголовок конструкции

        while len(text) > 0:

            m = search(pattern, text)
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
                new_node = Node(text[m.start():end_body], [])

            # если любая другая конструкция
            # парсим ее в глубину
            else:
                new_node = parse(text[start_body+1:end_body], new_header)

            node.subnodes.append(new_node)

            # удаляем обработанную часть текста
            # идем дальше
            text = text[end_body+1:]

            print(f'{node.data}', node.subnodes)

        return node

def print_tree(node, t=0):
    if node.data.startswith('Expr'):
        print('    '*t, f'{node.data}' + '}')
    else:
        print('    '*t, node.data, '{')
        for n in node.subnodes:
            print_tree(n, t+1)
        print('    '*t, '}')


if __name__ == '__main__':
    text = '''
    If(3 > 1){
        Expr{
            a = 11;
            b = a * 2;
            b = a * 3;
        }
        For(a=1;a<4;a=a+1;){
            Expr{
                b = a * 4;
            }
        }
        While(b>4){
            Expr{
                b=b-2;
            }
        }
    }
    Expr{
        c = 19;
    }
    '''
    text = text.replace('\n', '').replace(' ', '')
    header = 'Main'
    n = parse(text, header)
    #print_tree(n)
