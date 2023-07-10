from re import fullmatch, match, search, findall, compile
from constructions import *
from basic import *

class Node():
    def __init__(self, data: str, subnodes: list[Construction]=[]):
        self.data: str = data
        self.subnodes: list[Construction] = subnodes
        self.variables = {}

    def __repr__(self):
        return str(self.data) + ':' + str(self.subnodes)

class ConstructionTree():
    def __init__(self, root=None):
        self.root = root

    @classmethod
    def parse(text: str):
        m = search(pattern, text)
        start, end = m.start(), m.end()         # границы заголовка конструкции
        obj_text = text[start:end]              # заголовок

        index = end - 1
        stack = Stack()
        node = Node()

        node.data = obj_text                    # заголовок конструкции

        while index < len(text) - 1:            # ищем индекс конца данной
            index += 1                          # констркуции

            if text[index] == '{':
                stack.push('{')

            elif text[index] == '}':

                if not stack.is_empty():        # костыль. хз почему без него 
                    stack.pop()                 # не работает

                if stack.is_empty():
                    if obj_text == 'Expr':      # если Expr, то в глубину не парсим
                        print(text[end:index+1])
                        node.subnodes.append(Node(text[start:index+1], []))
                        end = index + 1 ###########3
                        start = end
                    else:                       # парсим в глубину
                        node.subnodes.append(parse(text[end:index+1]))

                    if text[index:].replace('}', '') == '':               # идем дальше в границах 
                        break

        # variables  в ноду, можно передавать из высших нод
        # класс Builder который создает конструкцию из ее заголовка 
        # разделить сложные конструкции на заголовок и тело
        return node

######
global constructions
constructions = {'Block': Block,                      # Все возможные конструкции
                 'If\(.*?\)': If,
                 'For\(.*?\)': For,
                 'Main': Main,
                 'While\(.*?\)': While,
                 'Expr': ExpressionBlock}
global pattern
pattern = compile('|'.join(_ for _ in constructions.keys()))   # Регулярка для нахождения первой конструкции что попадется
#####

    # variables  в ноду, можно передавать из высших нод
    # класс Builder который создает конструкцию из ее заголовка 
    # разделить сложные конструкции на заголовок и тело

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


# variables  в ноду, можно передавать из высших нод
# класс Builder который создает конструкцию из ее заголовка 
# разделить сложные конструкции на заголовок и тело
#print(node)

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
#n = Node()
header = 'Main'
n = parse(text, header)
#print_tree(n)
