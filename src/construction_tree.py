from re import fullmatch, match, search, findall, compile
from constructions import *
from basic import *


def parse(text: str, node):
    
    m = search(pattern, text)
    start, end = m.start(), m.end()
    obj_text = text[start:end]
    index = end
    stack = Stack()
    
    local_node = Node()

    if obj_text == 'Expr':
        node.data = ExpressionBlock(text, {})
        return node
        #print(text) # обработка блока
        #return #ExpressionBlock(text, variables)

    while index < len(text) - 1:
        index += 1
        if text[index] == '{':
            stack.push('{')
        elif text[index] == '}':
            if not stack.is_empty():
                stack.pop()
            if stack.is_empty():
                node.siblings.append(parse(text[end+1:index+1], local_node))
                #parse(text[end+1:index+1])
                break


    if len(text[index+1:-1]) > 0:
        node.siblings.append(parse(text[index+1:-1], local_node))
        #parse(text[index+1:-1])

    block = Block(node.siblings, {})
    obj = constructions[obj_text]
    node.data = obj(block) # где это должно стоять??

    # variables  в ноду, можно передавать из высших нод
    # класс Builder который создает конструкцию из ее заголовка 
    # разделить сложные конструкции на заголовок и тело

    return node

def parse(text: str):
    #text = text.strip()
    constructions = ['Block{',           # Все возможные конструкции
                     'If{',
                     'For{',
                     'While{',
                     'Expr{',
                     ]

    pattern = '|'.join(_ for _ in constructions)   # Регулярка для нахождения первой конструкции что попадется

    m = search(pattern, text)
    if m is None:
        return
    start, end = m.start(), m.end()
    obj = text[start:end]
    index = end
    stack = Stack()
    while index < len(text) - 1:
        index += 1
        if text[index] == '{':
            stack.push('{')
        elif text[index] == '}':
            if not stack.is_empty():
                stack.pop()
            if stack.is_empty():
                parse(text[end:index+1])
                break

    print(text)
    

class Node():
    def __init__(self, data: Construction='lol', siblings: list[Construction]=[]):
        self.data: Construction = data
        self.siblings: list[Construction] = siblings
        self.variables = {}

    def __repr__(self):
        return str(self.data) #+ ' ' + str(self.siblings)

class ConstructionTree():
    def __init__(self, root=None):
        self.root = root

    @classmethod
    def parse(cls, text: str, node, lst=[]):
        constructions = ['Block',                      # Все возможные конструкции
                         'If',
                         'For',
                         'Main',
                         'While',
                         'Expr']

        pattern = '|'.join(_ for _ in constructions)   # Регулярка для нахождения первой конструкции что попадется

        m = search(pattern, text)
        if m is None:
            return
        start, end = m.start(), m.end()
        obj = text[start:end]
        index = end
        stack = Stack()

        if obj == 'Block':
            print(text)
            return

        while index < len(text) - 1:
            index += 1
            if text[index] == '{':
                stack.push('{')
            elif text[index] == '}':
                if not stack.is_empty():
                    stack.pop()
                if stack.is_empty():
                    parse(text[end+1:index+1])
                    break


        parse(text[index+1:-1])

        return obj

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


def parse(text: str, node):
    m = search(pattern, text)

    #if m is None:                           # если больше нет совпадений
    #    return node                         # вернуть текущую ноду

    start, end = m.start(), m.end()         # границы заголовка конструкции
    obj_text = text[start:end]              # заголовок

    index = end
    stack = Stack()
    local_node = Node()


    while index < len(text) - 1:            # ищем индекс конца данной
        index += 1                          # констркуции
        if text[index] == '{':
            stack.push('{')
        elif text[index] == '}':

            if not stack.is_empty():        # костыль. хз почему без него 
                stack.pop()                 # не работает

            if stack.is_empty():
                if obj_text == 'Expr':      # если Expr, то в глубину не парсим
                    #print(text[start:index+1])
                    node.data = text[start:index+1]
                    #node.siblings.append(Node(text[start:index+1], []))
                else:                       # парсим в глубину
                    node.siblings.append(parse(text[end:index+1], local_node))
                break


    #if len(text[index:]) > 0:               # идем дальше в границах 
    if text[index:].replace('}', '') != '':               # идем дальше в границах 
        #print(text[index:])
                                            # конструкции в которой сейчас находимся
        node.siblings.append(parse(text[index:], local_node))


    if obj_text != 'Expr':
        node.data = obj_text                    # заголовок конструкции

    # variables  в ноду, можно передавать из высших нод
    # класс Builder который создает конструкцию из ее заголовка 
    # разделить сложные конструкции на заголовок и тело
    
    print(node.data, node.siblings)

    return node



text = '''
Main{ 
    If(3 > 1){
        For(a=1;a<4;a=a+1;){
            Expr{
                a = 11;
                b = a * 2;
                b = a * 3;
            }
        }
        Expr{
            1 + 2;
        }
        Expr{
            1 + 2;
        }
        While(b < 19){
            Expr{
                b = b + 1;
            }
        }
    }
    Expr{
        c = 19;
    }
}
'''
text = text.replace('\n', '').replace(' ', '')
n = Node()
parse(text, n)
print(n.siblings)
