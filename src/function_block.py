from re import search
from construction import Construction


class FunctionBlock(Construction): # не обязана наследоваться от конструкции. можно в парсинге дерева добавлять в хранилище
    regex: str = 'Func\(.*?\)'
    name: str = 'Func'

    def __init__(self, text: str):
        self.head = self.validate(text)

    def validate(self, text: str):
        m = search(self.regex, text)
        head: str = text[m.start():m.end()-1].replace('Func(', '')
        return head

    def __repr__(self):
        return 'fn#' + self.head

